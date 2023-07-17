import React, { useState } from "react";

export const login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const andleSubmit = async (event) => {
    event.preventDefault();

    const response = await fetch("http://localhost:8000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www.form-urlencoded",
      },
      body: new URLSearchParams({
        username,
        password,
      }),
    });
    const data = await response.json()
    
  };


  return <div>login</div>;
};
