import React,{useState,useEffect,createContext} from "react";
import AuthMessage from "./AuthMessage";

export const AuthContext = createContext();

function LoginForm(){

const [username,setUsername]=useState("")
const [password,setPassword]=useState("")
const [status,setStatus]=useState(null)

const handleLogin = (e) => {
  e.preventDefault(); // ⚡ Stop form submission
  if (username === "" || password === "") {
    setStatus({ type: "error", message: "Fields cannot be empty" });
    return;
  }
  if (password.length < 8) {
    setStatus({ type: "error", message: "Password must be at least 8 characters" });
    return;
  }

  fetch("https://jsonplaceholder.typicode.com/users")
    .then(res => res.json())
    .then(data => {
      const user = data.find(u => u.username === username);

      // ⚠ jsonplaceholder doesn't have 'password', using email as password here
      if (user && user.email === password) {
        setStatus({ type: "success", message: "Login successful" });
        setTimeout(() => window.location = "/flavors", 2000);
      } else {
        setStatus({ type: "error", message: "Invalid credentials" });
      }
    });
};

return(

<AuthContext.Provider value={{status}}>

<div className="login-form">
<form>
<h2 className="login-title">Login</h2>

<label >Username </label>
<input
className="login-input"
placeholder="Username"
onChange={(e)=>setUsername(e.target.value)}
/>
<br/><br/>
<label>Password </label>
<input
className="login-input"
type="password"
placeholder="Password"
onChange={(e)=>setPassword(e.target.value)}
/>
<br/>
<button 
className="login-button"
onClick={handleLogin}
>
Login
</button>

<p className="forgot-password">Forgot Password?</p>

<AuthMessage/>
</form>
</div>

</AuthContext.Provider>

)

}

export default LoginForm;