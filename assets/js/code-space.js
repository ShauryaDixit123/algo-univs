import React from "react";

import { Breadcrumb, Layout, Menu, theme } from "antd";
import axios from "axios";
import { notification } from "antd";
import { useSearchParams } from "react-router-dom";
import { Space, Table, Tag, Flex, TextArea, Input, Button, Select } from "antd";
import { sideNavItems, navItems, testColumn } from "./constants/space-items";
import { RenderIde } from "./components/blocks";

const { Header, Content, Sider } = Layout;

const columnItems = (onClickAction) => [
  {
    title: "Title",
    dataIndex: "name",
    key: "name",
    render: (text, record) => (
      <span
        style={{
          color: "#1677FF",
          fontWeight: "500",
          fontSize: "18px",
          cursor: "pointer",
        }}
        onClick={() => {
          console.log(record, "record");
          onClickAction(record.id);
        }}
      >
        {text}
      </span>
    ),
  },
  {
    title: "Rating",
    dataIndex: "rating",
    key: "rating",
    render: (text) => (
      <span style={{ color: "#1677FF", fontWeight: "500", fontSize: "14px" }}>
        {text}
      </span>
    ),
  },
  {
    title: "Tags",
    key: "tags",
    dataIndex: "tags",
    render: (_, { type }) => (
      <>
        {type.map((tag) => {
          let color = tag.length > 5 ? "geekblue" : "green";
          if (tag === "dynamic programming") {
            color = "volcano";
          }
          return (
            <Tag color={color} key={tag}>
              {tag.type.toUpperCase()}
            </Tag>
          );
        })}
      </>
    ),
  },
];

const CodeSpaces = () => {
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

  const [currentState, setCurrentState] = React.useState("Problems");
  const [currentSelectedProblem, setCurrentSelectedProblem] = React.useState();
  const [currentSelectedProblemInfo, setCurrentSelectedProblemInfo] =
    React.useState();
  const [problems, setProblems] = React.useState([]);
  React.useEffect(() => {
    fetchAllProblems();
  }, []);
  React.useEffect(() => {
    currentSelectedProblem && handleFetchProblemDetails(currentSelectedProblem);
  }, [currentSelectedProblem]);
  console.log(currentSelectedProblemInfo, currentSelectedProblem, "problems");
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
            console.log("sadasdasds");
            setCurrentState(info);
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
            items={sideNavItems}
          />
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Breadcrumb style={{ margin: "16px 0" }}>
            <Breadcrumb.Item>{currentState}</Breadcrumb.Item>
            <Breadcrumb.Item>
              {currentSelectedProblem || "List"}
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
            ) : null}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default CodeSpaces;
