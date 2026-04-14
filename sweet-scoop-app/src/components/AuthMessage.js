import React, { useContext } from "react";
import { AuthContext } from "./LoginForm";
import DisplayStatus from "./DisplayStatus";

function AuthMessage() {
  const context = useContext(AuthContext);
  if (!context || !context.status) return null;

  return <DisplayStatus type={context.status.type} message={context.status.message} />;
}

export default AuthMessage;