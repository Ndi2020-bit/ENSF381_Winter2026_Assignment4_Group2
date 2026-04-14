// src/components/OrderItem.js
import React from "react";

function OrderItem({ item, removeFromOrder }) {
  return (
    <div className="order-item">
      <h4>{item.name}</h4>
      <p>Quantity: {item.quantity}</p>
      <p>Price: ${(item.price * item.quantity).toFixed(2)}</p>
      <button onClick={() => removeFromOrder(item.id)}>Remove Item</button>
    </div>
  );
}

export default OrderItem;