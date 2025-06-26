import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { CssBaseline, Container } from "@mui/material";


import ContextForm from "./pages/ContextForm";

import Recommendations from "./pages/Recommendations";
import Login from "./pages/login";

const App: React.FC = () => {
  const token = localStorage.getItem("token");

  return (
    <>
      <CssBaseline />
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <Routes>
          <Route path="/" element={token ? <Navigate to="/context" /> : <Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/context" element={token ? <ContextForm /> : <Navigate to="/login" />} />
          <Route path="/recommendations" element={token ? <Recommendations /> : <Navigate to="/login" />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Container>
    </>
  );
};

export default App;
