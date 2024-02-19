import React from "react";
import Input from "antd/lib/input";
import UserDetailsModal from "./components/blocks";
import Flex from "antd/lib/grid/row";
import { useState } from "react";
import CodeSpaces from "./code-space";
import { notification, Space } from "antd";
import axios from "axios";
import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";

export const App = () => {
  const [username, setUsername] = useState("");
  const handleCreateNewUser = async (user) => {
    try {
      const reqURL = "http://localhost:8000/polls/create_user";
      console.log(user, "username");
      const form = new FormData();
      const data = {
        name: user,
      };
      form.append("data", JSON.stringify(data));
      const res = await axios.post(reqURL, form);
      console.log(res, "234234324234");
      notification.message({
        message: "Success",
        description: "User created successfully!",
      });
    } catch (error) {
      // notification.error({
      //   message: "Error",
      //   description: "Error in creating user",
      // });
      console.log(error, "error");
    }
  };
  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <Flex
        justify="center"
        style={{ fontSize: "30px", padding: "2rem", backgroundColor: "wheat" }}
      >
        {username && `Welcome, ${username} to `}{" "}
        <Space style={{ fontWeight: "600" }}> {"{{'CODE DORM'}}"} </Space>
        <span style={{ fontWeight: "400", fontSize: "12px" }}>
          (Party hosted by Shaurya Dixit)
        </span>
      </Flex>
      <UserDetailsModal
        onCancel={() => {
          if (!username) {
            setUsername("Guest");
          }
        }}
        onOk={async (username) => {
          await handleCreateNewUser(username);
          setUsername(username);
        }}
      />
      <CodeSpaces />
    </div>
  );
};
