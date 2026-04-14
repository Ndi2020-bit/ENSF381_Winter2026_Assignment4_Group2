import json
import bcrypt
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

users = [
# { 
#   "id": 1, 
#   "username": "sweet_alice", 
#   "email": "alice@example.com", 
#   "password_hash": "$2b$12$examplehashedvalue", 
#   "cart": [ 
#     { 
#       "flavorId": 2, 
#       "name": "Chocolate Bliss", 
#       "price": 5.49, 
#       "quantity": 2 
#     } 
#   ], 
#   "orders": [ 
#     { 
#       "orderId": 1, 
#       "items": [ 
#         { 
#           "flavorId": 1, 
#           "name": "Vanilla Dream", 
#           "price": 4.99, 
#           "quantity": 1 
#         } 
#       ], 
#       "total": 4.99, 
#       "timestamp": "2026-03-30 18:30:00" 
#     } 
#   ] 
# } 
]

def is_valid_email(email):
    # Basic regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    # Requirements: 8+ chars, 1 upper, 1 lower, 1 digit, 1 special
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 1. Validation: Length and Characters for Username
    if not username or not (3 <= len(username) <= 20):
        return jsonify({"success": False, "message": "Username must be 3-20 characters."}), 400
    if not re.match(r"^[A-Za-z][A-Za-z0-9_-]*$", username):
        return jsonify({"success": False, "message": "Invalid username format."}), 400

    # 2. Validation: Email and Password format
    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400
    if not is_valid_password(password):
        return jsonify({"success": False, "message": "Password does not meet requirements."}), 400

    # 3. Check for Duplicates
    if any(u['username'] == username for u in users):
        return jsonify({"success": False, "message": "Username is already taken."}), 400
    if any(u['email'] == email for u in users):
        return jsonify({"success": False, "message": "Email is already registered."}), 400

    # 4. Hash the Password
    # bcrypt requires bytes, so we encode the string
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # 5. Store the User
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "email": email,
        "password_hash": hashed_pw.decode('utf-8'), # Store as string in JSON-like list
        "cart": [],
        "orders": []
    }
    users.append(new_user)

    return jsonify({"success": True, "message": "Registration successful."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 1. Find the user in our in-memory list
    user = next((u for u in users if u['username'] == username), None)

    # 2. If user exists, check the password
    if user:
        # bcrypt.checkpw requires bytes: 
        # - The plain password from the request
        # - The hashed password from our "database"
        password_bytes = password.encode('utf-8')
        hash_bytes = user['password_hash'].encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_bytes):
            # 3. Success! Return the data the frontend needs for the session
            return jsonify({
                "success": True,
                "message": "Login successful.",
                "userId": user['id'],
                "username": user['username']
            }), 200

    # 4. If user not found OR password didn't match, return generic error
    return jsonify({
        "success": False,
        "message": "Invalid username or password."
    }), 401

@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        # 1. Read the data from the JSON file
        with open('backend/reviews.json', 'r') as f:
            all_reviews = json.load(f)
        
        # 2. Select 2 random reviews
        # If there are fewer than 2 reviews, return all of them
        sample_size = min(len(all_reviews), 2)
        random_reviews = random.sample(all_reviews, sample_size)
        
        # 3. Return the success response
        return jsonify({
            "success": True,
            "message": "Reviews loaded.",
            "reviews": random_reviews
        }), 200

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "message": "Reviews file not found."
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/flavors', methods=['GET'])
def get_flavors():
    try:
        # 1. Read the data from flavors.json
        # Make sure the path matches your backend folder structure
        with open('backend/flavors.json', 'r') as f:
            all_flavors = json.load(f)
        
        # 2. Return the full list of flavors
        return jsonify({
            "success": True,
            "message": "Flavors loaded.",
            "flavors": all_flavors
        }), 200

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "message": "Flavors file not found."
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500

@app.route('/cart', methods=['GET'])
def get_cart():
    # 1. Get the userId from the query string (?userId=3)
    user_id_str = request.args.get('userId')
    
    if not user_id_str:
        return jsonify({"success": False, "message": "userId is required."}), 400

    try:
        user_id = int(user_id_str)
        # 2. Find the user in our in-memory list
        user = next((u for u in users if u['id'] == user_id), None)

        if user:
            return jsonify({
                "success": True,
                "message": "Cart loaded.",
                "cart": user['cart']  # Return the user's specific cart list
            }), 200
        else:
            return jsonify({"success": False, "message": "User not found."}), 404

    except ValueError:
        return jsonify({"success": False, "message": "Invalid userId format."}), 400

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('userId')
    flavor_id = data.get('flavorId')

    # 1. Validate User exists
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # 2. Validate Flavor exists (Read from flavors.json)
    try:
        with open('backend/flavors.json', 'r') as f:
            flavors = json.load(f)
        flavor = next((f for f in flavors if f['id'] == flavor_id), None)
        
        if not flavor:
            return jsonify({"success": False, "message": "Flavor not found."}), 404

        # 3. Check if flavor is already in the cart
        cart_item = next((item for item in user['cart'] if item['flavorId'] == flavor_id), None)
        
        if cart_item:
            # Assignment requirement: Error if already exists
            return jsonify({
                "success": False, 
                "message": "Flavor already in cart. Use PUT to update quantity."
            }), 400

        # 4. Add new item to cart
        new_item = {
            "flavorId": flavor['id'],
            "name": flavor['name'],
            # Ensure price is a float if it's stored as a string "$4.99"
            "price": float(flavor['price'].replace('$', '')) if isinstance(flavor['price'], str) else flavor['price'],
            "quantity": 1
        }
        
        user['cart'].append(new_item)

        return jsonify({
            "success": True,
            "message": "Flavor added to cart.",
            "cart": user['cart']
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/cart', methods=['PUT'])
def update_cart():
    data = request.get_json()
    user_id = data.get('userId')
    flavor_id = data.get('flavorId')
    quantity = data.get('quantity')

    # 1. Validate User exists
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # 2. Validate Quantity is at least 1
    if quantity is None or not isinstance(quantity, int) or quantity < 1:
        return jsonify({"success": False, "message": "Quantity must be at least 1."}), 400

    # 3. Find the flavor in the USER'S cart (not the general flavor list)
    cart_item = next((item for item in user['cart'] if item['flavorId'] == flavor_id), None)
    
    if not cart_item:
        return jsonify({
            "success": False, 
            "message": "Flavor not found in cart."
        }), 404

    # 4. Update the quantity
    cart_item['quantity'] = quantity

    return jsonify({
        "success": True,
        "message": "Cart updated successfully.",
        "cart": user['cart']
    }), 200

@app.route('/cart', methods=['DELETE'])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get('userId')
    flavor_id = data.get('flavorId')

    # 1. Validate User exists
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # 2. Remove the flavor from the cart
    # We redefine the cart list by keeping everything EXCEPT the flavorId we want to delete
    original_length = len(user['cart'])
    user['cart'] = [item for item in user['cart'] if item['flavorId'] != flavor_id]

    # 3. Check if something was actually removed
    if len(user['cart']) == original_length:
        return jsonify({"success": False, "message": "Flavor not found in cart."}), 404

    return jsonify({
        "success": True,
        "message": "Flavor removed from cart.",
        "cart": user['cart']
    }), 200

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    user_id = data.get('userId')

    # 1. Validate User exists
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # 2. Validate Cart is not empty
    if not user['cart']:
        return jsonify({"success": False, "message": "Cart is empty."}), 400

    # 3. Create the order object
    # Calculate total price (optional, but good for history)
    order_total = sum(item['price'] * item['quantity'] for item in user['cart'])
    
    new_order = {
        "orderId": len(user['orders']) + 1,
        "items": list(user['cart']),  # Copy the current cart items
        "total": round(order_total, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 4. Save to order history and CLEAR the cart
    user['orders'].append(new_order)
    user['cart'] = []  # Empty the cart list

    return jsonify({
        "success": True,
        "message": "Order placed successfully.",
        "orderId": new_order['orderId']
    }), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    # 1. Get the userId from the query string (?userId=3)
    user_id_str = request.args.get('userId')
    
    if not user_id_str:
        return jsonify({"success": False, "message": "userId is required."}), 400

    try:
        user_id = int(user_id_str)
        # 2. Find the user
        user = next((u for u in users if u['id'] == user_id), None)

        if user:
            # 3. Return the order history (it's already an empty list [] by default)
            return jsonify({
                "success": True,
                "message": "Order history loaded.",
                "orders": user['orders']
            }), 200
        else:
            return jsonify({"success": False, "message": "User not found."}), 404

    except ValueError:
        return jsonify({"success": False, "message": "Invalid userId format."}), 400

if __name__ == '__main__':
    app.run(debug=True) #port=5000?
