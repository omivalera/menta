import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const ContextForm: React.FC = () => {
  const [form, setForm] = useState({
    mood: "",
    note: "",
    location: "",
    weather: "",
    activity_level: "",
    sleep_hours: "",
  });

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("No token");

      // Parse numbers for activity_level and sleep_hours
      const payload = {
        ...form,
        activity_level: parseFloat(form.activity_level),
        sleep_hours: parseFloat(form.sleep_hours),
      };

      await axios.post("http://localhost:8000/context", payload, {
        headers: { Authorization: `Bearer ${token}` },
      });

      alert("Contexto registrado");
      navigate("/recommendations");
    } catch (err) {
      alert("Error al registrar contexto");
    }
  };

  return (
    <Box sx={{ maxWidth: 500, mx: "auto", mt: 4 }}>
      <Typography variant="h5" mb={2}>
        Registrar tu contexto emocional
      </Typography>
      {["mood", "note", "location", "weather", "activity_level", "sleep_hours"].map((field) => (
        <TextField
          key={field}
          fullWidth
          margin="normal"
          label={field.replace("_", " ").toUpperCase()}
          name={field}
          value={form[field as keyof typeof form]}
          onChange={handleChange}
        />
      ))}
      <Button variant="contained" fullWidth onClick={handleSubmit} sx={{ mt: 2 }}>
        Enviar
      </Button>
    </Box>
  );
};

export default ContextForm;
