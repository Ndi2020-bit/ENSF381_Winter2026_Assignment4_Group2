import React from "react";

function DisplayStatus({ type, message }) {
  const style = {
    color: type === "success" ? "green" : "red",
    fontWeight: "bold",
    marginTop: "10px",
  };

  return <p style={style}>{message}</p>;
}

export default DisplayStatus;