// src/components/OrderList.js
import React, { useEffect, useState } from "react";
import OrderItem from "./OrderItem";

function OrderList({ order, setOrder }) {
  const removeFromOrder = (id) => {
    setOrder((prev) => {
      const item = prev.find((i) => i.id === id);
      if (item.quantity > 1) {
        return prev.map((i) =>
          i.id === id ? { ...i, quantity: i.quantity - 1 } : i
        );
      } else {
        return prev.filter((i) => i.id !== id);
      }
    });
  };

  const totalPrice = order.reduce((sum, item) => sum + item.price * item.quantity, 0);

  // Save/load from localStorage
  useEffect(() => {
    const savedOrder = localStorage.getItem("iceCreamOrder");
    if (savedOrder) {
      setOrder(JSON.parse(savedOrder));
    }
  }, [setOrder]);

  useEffect(() => {
    localStorage.setItem("iceCreamOrder", JSON.stringify(order));
  }, [order]);

  return (
    <>
    <h3>Your Order</h3>
    <div className="order-list">
      
      {order.length === 0 && <p>No items in your order.</p>}
      {order.map((item) => (
<OrderItem key={item.id} item={item} removeFromOrder={removeFromOrder} />      ))}
      {order.length > 0 && <h4>Total: ${totalPrice.toFixed(2)}</h4>}
    </div>
    </>
  );
}

export default OrderList;