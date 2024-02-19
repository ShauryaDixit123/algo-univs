import React from "react";
import {
  LaptopOutlined,
  NotificationOutlined,
  UserOutlined,
} from "@ant-design/icons";

export const sideNavItems = [
  {
    key: `Your attempts`,
    icon: React.createElement(UserOutlined),
    label: `Your attempts`,

    children: [],
  },
  {
    key: `IDE`,
    icon: React.createElement(NotificationOutlined),
    label: `IDE`,
  },
  {
    key: `Create Problem`,
    icon: React.createElement(NotificationOutlined),
    label: `Create Problem`,
  },
];

export const navItems = [
  {
    key: 1,
    icon: React.createElement(LaptopOutlined),
    label: `Home`,
  },
  {
    key: 2,
    icon: React.createElement(LaptopOutlined),
    label: `Problems`,
  },
];

export const testColumn = (children) => [
  {
    key: "Test Cases",
    label: "Test Cases",
    icon: React.createElement(NotificationOutlined),
    children: children,
  },
];
