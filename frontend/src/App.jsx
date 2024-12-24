import React, { useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import AuthContext from "./helpers/AuthContext";
import {
  Home,
  Login,
  Product,
  AuthVerify,
  Checkout,
  Policies,
  PaymentStatus,
} from "./pages";
import { Loader, Navbar } from "./components";

const App = () => {
  const authCtx = useContext(AuthContext);
  if (!authCtx.isAuthChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen md:h-screen p-4 md:p-8 text-primary">
      <Router>
        <Navbar />
        <Routes>
          <Route
            path="/login"
            element={!authCtx.isLoggedIn ? <Login /> : <Navigate to="/" />}
          />
          <Route
            path="/product/:id"
            element={
              <Product />
            }
          />
          <Route
            path="/checkout"
            element={
              authCtx.isLoggedIn ? <Checkout /> : <Navigate to="/login" />
            }
          />
          <Route path="/policies" element={<Policies />} />
          <Route
            path="/"
            element={
              <Home user={
                authCtx.isLoggedIn ? authCtx.user : null
              } />
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
          <Route path="/authVerify" element={<AuthVerify />} />
          <Route
            path="/payment-status"
            element={
              authCtx.isLoggedIn ? <PaymentStatus /> : <Navigate to="/login" />
            }
          />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
