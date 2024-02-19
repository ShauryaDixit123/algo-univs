import React from "react";
import Modal from "antd/lib/modal";
import { useState } from "react";
import {
  Space,
  Table,
  Tag,
  Flex,
  TextArea,
  Menu,
  Input,
  Button,
  Select,
} from "antd";
import { testColumn } from "../constants/space-items";
import { notification } from "antd";
import axios from "axios";

const UserDetailsModal = (props) => {
  const [visible, setVisible] = useState(true);
  const [username, setUsername] = useState("");
  return (
    <>
      <Modal
        onOk={() => {
          setVisible(false);
          props.onOk(username);
        }}
        title="Hi, new or been here? "
        closeIcon={false}
        open={visible}
      >
        <Input
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Your DORM's username or Try with entering something unique"
        />
      </Modal>
    </>
  );
};

export const RenderIde = (props) => {
  const { TextArea } = Input;
  const [selectedLang, setSelectedLang] = useState("py");
  const [code, setCode] = useState("");
  const currentSelectedProblemInfo = props.currentSelectedProblemInfo;
  const handleSubmitCode = async () => {
    console.log("submitting code");
    const reqURL = `http://localhost:8000/polls/compile_code_by_pid`;
    try {
      const form = new FormData();
      const data = {
        pid: currentSelectedProblemInfo?.id,
        uid: 1,
        sol: code,
        lang: selectedLang,
      };
      form.append("data", JSON.stringify(data));
      const res = await axios.post(reqURL, form);
      console.log(res.data, "reszxczxcxz");
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };
  console.log(currentSelectedProblemInfo, "currentSelectedProblemInfo");
  return (
    <>
      <Flex vertical>
        <h1>
          {currentSelectedProblemInfo?.name}
          <span style={{ fontSize: "14px", marginLeft: "10px" }}>
            Rating: ({currentSelectedProblemInfo?.rating}/5)
          </span>
        </h1>

        <Flex style={{ width: "100%" }} align="center" justify="space-between">
          <h2>{currentSelectedProblemInfo?.des}</h2>
        </Flex>
        <Flex gap={10}>
          <Select
            defaultValue={selectedLang}
            onChange={(val) => setSelectedLang(val)}
            style={{ width: 120 }}
            options={[
              { value: "py", label: "Python" },
              { value: "java", label: "Java" },
              { value: "c", label: "C" },
            ]}
          />
          <Button
            onClick={handleSubmitCode}
            style={{ backgroundColor: "#1677FF", color: "white" }}
          >
            Run
          </Button>
        </Flex>
        <Flex>
          <TextArea
            onChange={(e) => setCode(e.target.value)}
            style={{ minHeight: "440px", marginTop: "1rem" }}
          />
          <Menu
            mode="inline"
            defaultSelectedKeys={["Test Cases"]}
            defaultOpenKeys={["Test Cases"]}
            style={{ height: "100%", borderRight: 0, flex: "0.4" }}
            items={testColumn(
              currentSelectedProblemInfo?.test_cases.map((val, i) => ({
                ...val,
                key: i,
                label: (
                  <>
                    {" "}
                    Inp : <span style={{ color: "#1677FF" }}>{val.inp}</span>,
                    Out : <span style={{ color: "#1677FF" }}>{val.out}</span>
                  </>
                ),
              }))
            )}
          />
        </Flex>
      </Flex>
    </>
  );
};

export default UserDetailsModal;
