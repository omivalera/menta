import React, { useEffect, useState } from "react";
import { Typography, Box, List, ListItem, ListItemText, CircularProgress } from "@mui/material";
import axios from "axios";

const Recommendations: React.FC = () => {
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("No token");

        const res = await axios.get("http://localhost:8000/plans", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setRecommendations(res.data);
      } catch {
        alert("Error al obtener recomendaciones");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4 }}>
      <Typography variant="h5" mb={2}>
        Recomendaciones personalizadas
      </Typography>
      <List>
        {recommendations.length === 0 ? (
          <Typography>No hay recomendaciones disponibles.</Typography>
        ) : (
          recommendations.map((rec, idx) => (
            <ListItem key={idx}>
              <ListItemText primary={rec} />
            </ListItem>
          ))
        )}
      </List>
    </Box>
  );
};

export default Recommendations;
