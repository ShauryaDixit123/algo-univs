import React from "react";
import {
  LaptopOutlined,
  NotificationOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Tag } from "antd";

export const sideNavItems = (attemptedChildren, onClick) => [
  {
    key: `Your attempts`,
    icon: React.createElement(UserOutlined),
    label: `Your attempts`,

    children: attemptedChildren,
  },
  {
    key: `IDE`,
    icon: React.createElement(NotificationOutlined),
    label: `IDE`,
  },
  {
    key: `Create Problem`,
    icon: React.createElement(NotificationOutlined),
    label: "Create Problem",
  },
];

export const navItems = [
  {
    key: `Home`,
    icon: React.createElement(LaptopOutlined),
    label: `Home`,
  },
  {
    key: `Problems`,
    icon: React.createElement(LaptopOutlined),
    label: `Problems`,
  },
];

export const testColumn = (testCaseChildren, resultChildren) => [
  {
    key: "Test Cases",
    label: "Test Cases",
    icon: React.createElement(NotificationOutlined),
    children: testCaseChildren,
  },
  {
    key: "Result",
    label: "Result",
    icon: React.createElement(NotificationOutlined),
    children: resultChildren,
  },
];
export const columnItems = (onClickAction) => [
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
