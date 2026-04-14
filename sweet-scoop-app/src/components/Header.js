import { Link } from "react-router-dom";

function Header() {
  return (
    <>
      <header>
        <img src="/images/logo.webp" alt="Sweet Scoop" />
        <h1>Sweet Scoop Ice Cream Shop</h1>
      </header>

      <div className="navbar">
        <Link to="/">Home</Link>
        <Link to="/flavors">Flavors</Link>
        <Link to="/login">Login</Link>
      </div>
    </>
  );
}

export default Header;