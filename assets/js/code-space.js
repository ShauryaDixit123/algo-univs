import React from "react";

import { Breadcrumb, Layout, Menu, theme } from "antd";
import axios from "axios";
import { notification } from "antd";
import { useSearchParams } from "react-router-dom";
import { Space, Table, Tag, Flex, TextArea, Input, Button, Select } from "antd";
import {
  sideNavItems,
  navItems,
  testColumn,
  columnItems,
} from "./constants/space-items";
import { RenderIde } from "./components/blocks";

const { Header, Content, Sider } = Layout;

const CodeSpaces = () => {
  const userD = JSON.parse(localStorage.getItem("user"));
  const fetchAllProblems = async () => {
    const reqURL = "http://localhost:8000/polls/problem_list";
    try {
      const res = await axios.get(reqURL);
      setProblems(res.data);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };

  const handleFetchProblemDetails = async (id) => {
    const reqURL = `http://localhost:8000/polls/problem/${id}`;
    try {
      const res = await axios.get(reqURL);
      setCurrentSelectedProblemInfo(res.data);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };
  const handleFetchAllUserAttempts = async () => {
    const reqURL = `http://localhost:8000/polls/user_attempts/${userD.id}`;
    try {
      const res = await axios.get(reqURL);
      console.log(res.data, "user attempts");
      setAttemptedProblems(res.data);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };
  const [currentState, setCurrentState] = React.useState("Problems");
  const [currentSelectedProblem, setCurrentSelectedProblem] = React.useState();
  const [currentSelectedProblemInfo, setCurrentSelectedProblemInfo] =
    React.useState();
  const [problems, setProblems] = React.useState([]);
  const [attemptedProblems, setAttemptedProblems] = React.useState([]);

  React.useEffect(() => {
    currentState === "Problems" && fetchAllProblems();
    handleFetchAllUserAttempts();
  }, [currentState]);
  React.useEffect(() => {
    currentSelectedProblem &&
      (setCurrentState("IDE"),
      handleFetchProblemDetails(currentSelectedProblem));
  }, [currentSelectedProblem]);
  console.log(
    currentSelectedProblemInfo,
    currentSelectedProblem,
    currentState,
    "problemszxczx"
  );
  return (
    <Layout style={{ height: "100%", width: "100%" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={["2"]}
          items={navItems}
          style={{ flex: 1, minWidth: 0 }}
          onClick={(info) => {
            info.key === "2" && setCurrentState("Problems"),
              info.key === "1" && setCurrentState("Home");
          }}
        />
      </Header>
      <Layout>
        <Sider width={200}>
          <Menu
            mode="inline"
            selectedKeys={[currentState]}
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["Your attempts"]}
            style={{ height: "100%", borderRight: 0 }}
            items={sideNavItems(
              attemptedProblems?.map((val, i) => ({
                ...val,
                key: i,
                label: (
                  <div onClick={() => setCurrentSelectedProblem(val.pid_id)}>
                    {" "}
                    <span style={{ color: "#CCCCC" }}>{val.name}</span>,
                    <span style={{ color: "#1677FF" }}>{val.des}</span>
                  </div>
                ),
              }))
            )}
          />
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Breadcrumb style={{ margin: "16px 0" }}>
            <Breadcrumb.Item>{currentState}</Breadcrumb.Item>
            <Breadcrumb.Item>
              {currentState == "Problems" ? "List" : currentSelectedProblem}
            </Breadcrumb.Item>
          </Breadcrumb>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: "60%",
              borderRadius: "6px",
              backgroundColor: "white",
            }}
          >
            {currentState === "Problems" ? (
              <>
                <h1>Problems</h1>
                <Table
                  columns={columnItems(
                    (rec) => (
                      setCurrentSelectedProblem(rec), setCurrentState("IDE")
                    )
                  )}
                  dataSource={problems}
                />
              </>
            ) : currentState === "IDE" ? (
              <RenderIde
                currentSelectedProblemInfo={currentSelectedProblemInfo}
              />
            ) : currentState === "Home" ? (
              <></>
            ) : currentState === "Create Problem" ? (
              <></>
            ) : null}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default CodeSpaces;
