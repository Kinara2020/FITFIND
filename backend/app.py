from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FeatureExtractor
from similarity_search import SimilaritySearch
from database.db_connect import get_connection

app = Flask(__name__)
CORS(app)

# Load AI models once at startup
print("Loading AI models...")
searcher = SimilaritySearch()
print("✅ Ready to serve requests")

@app.route('/api/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    temp_path = "temp_query.jpg"
    file.save(temp_path)
    
    start_time = time.time()
    similar_ids = searcher.search(temp_path, top_k=5)
    time_taken = int((time.time() - start_time) * 1000)
    
    conn = get_connection()
    cur = conn.cursor()
    
    results = []
    for item in similar_ids:
        cur.execute("""
            SELECT product_id, name, category, 
                   sub_category, color, gender
            FROM products 
            WHERE product_id = %s
        """, (item['product_id'],))
        row = cur.fetchone()
        if row:
            results.append({
                'product_id': row[0],
                'name': row[1],
                'category': row[2],
                'sub_category': row[3],
                'color': row[4],
                'gender': row[5],
                'similarity_score': round(item['similarity_score'], 4),
                'image_url': f"/images/{row[0]}.jpg"
            })
    
    cur.execute("""
        INSERT INTO searches (query_image_path, top_results, searched_at)
        VALUES (%s, %s::jsonb, NOW())
        RETURNING search_id
    """, (temp_path, str(results).replace("'", '"')))
    
    search_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    os.remove(temp_path)
    
    return jsonify({
        'results': results,
        'search_id': search_id,
        'time_taken_ms': time_taken
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category', '')
    color = request.args.get('color', '')
    gender = request.args.get('gender', '')
    page = int(request.args.get('page', 1))
    limit = 20
    offset = (page - 1) * limit
    
    conn = get_connection()
    cur = conn.cursor()
    
    query = "SELECT product_id, name, category, color, gender FROM products WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = %s"
        params.append(category)
    if color:
        query += " AND color = %s"
        params.append(color)
    if gender:
        query += " AND gender = %s"
        params.append(gender)
    
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    cur.execute(query, params)
    rows = cur.fetchall()
    
    products = [{
        'product_id': r[0],
        'name': r[1],
        'category': r[2],
        'color': r[3],
        'gender': r[4],
        'image_url': f"/images/{r[0]}.jpg"
    } for r in rows]
    
    cur.close()
    conn.close()
    return jsonify({'products': products, 'page': page})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT product_id, name, category, 
               sub_category, color, gender
        FROM products WHERE product_id = %s
    """, (product_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'product_id': row[0],
        'name': row[1],
        'category': row[2],
        'sub_category': row[3],
        'color': row[4],
        'gender': row[5],
        'image_url': f"/images/{row[0]}.jpg"
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM searches")
    total_searches = cur.fetchone()[0]
    
    cur.execute("""
        SELECT COUNT(*) FROM searches 
        WHERE DATE(searched_at) = CURRENT_DATE
    """)
    searches_today = cur.fetchone()[0]
    
    cur.execute("""
        SELECT category, COUNT(*) as total
        FROM products GROUP BY category
        ORDER BY total DESC LIMIT 1
    """)
    top_category = cur.fetchone()
    
    cur.execute("""
        SELECT color, COUNT(*) as total
        FROM products GROUP BY color
        ORDER BY total DESC LIMIT 1
    """)
    top_color = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'total_searches': total_searches,
        'searches_today': searches_today,
        'top_category': top_category[0] if top_category else None,
        'most_searched_color': top_color[0] if top_color else None
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT category, COUNT(*) as total
        FROM products
        GROUP BY category
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        'categories': [{'name': r[0], 'total': r[1]} for r in rows]
    })

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('../data/images', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)