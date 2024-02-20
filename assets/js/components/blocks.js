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
import { handleConvert, handleTabKeyUp } from "../helper";

const UserDetailsModal = (props) => {
  const [visible, setVisible] = useState(props.open);
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
  const [openRating, setOpenRating] = useState(false);
  const [code, setCode] = useState("");
  const [testCaseRes, setTestCaseRes] = useState([]);
  const currentSelectedProblemInfo = props.currentSelectedProblemInfo;
  const userD = JSON.parse(localStorage.getItem("user"));
  const [problemRating, setProblemRating] = useState(0);
  const textAreaRef = React.useRef();
  const handleSubmitCode = async () => {
    const reqURL = `http://16.171.55.5/polls/compile_code_by_pid`;
    try {
      const form = new FormData();
      const data = {
        pid: currentSelectedProblemInfo?.id,
        uid: userD.id,
        sol: code,
        lang: selectedLang,
      };
      form.append("data", JSON.stringify(data));
      const res = await axios.post(reqURL, form);
      console.log(res.data.result, "resasdasdas");
      res.data.passed && setOpenRating(true);
      setTestCaseRes(res.data.result);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in submitting solution",
      });
    }
  };
  const handleFetchUserHistoryForProblem = async () => {
    const reqURL = `http://16.171.55.5/polls/user_sol`;
    const form = new FormData();
    const data = {
      pid: currentSelectedProblemInfo?.id,
      uid: userD.id,
    };
    form.append("data", JSON.stringify(data));
    try {
      const res = await axios.post(reqURL, form);
      console.log(res, "user history");
      const data = res.data;
      setCode(data.sol);
      setTestCaseRes(data.tst_hstry);
      setSelectedLang(data.lang);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };
  const handleSubmitRating = async () => {
    try {
      const reqURL = `http://16.171.55.5/polls/rate_problem`;
      const form = new FormData();
      const data = {
        pid: currentSelectedProblemInfo?.id,
        uid: userD.id,
        rating: problemRating,
      };
      form.append("data", JSON.stringify(data));
      const res = await axios.post(reqURL, form);
      console.log(res, "rating");
      setOpenRating(false);
    } catch (error) {
      notification.error({
        message: "Error",
        description: "Error in fetching problems",
      });
    }
  };
  console.log(currentSelectedProblemInfo, "currentSelectedProblemInfo");
  React.useEffect(() => {
    currentSelectedProblemInfo?.id && handleFetchUserHistoryForProblem();
  }, [currentSelectedProblemInfo]);
  return (
    <>
      <Modal
        onOk={handleSubmitRating}
        title="Congrats! All cases are solved!"
        open={openRating}
        onCancel={() => setOpenRating(false)}
      >
        <h1>Rate the problem</h1>
        <Input
          onChange={(e) => setProblemRating(e.target.value)}
          min={0}
          max={5}
          type="number"
        />
      </Modal>
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
            value={selectedLang}
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
            ref={textAreaRef}
            onChange={(e) => setCode(e.target.value)}
            value={code}
            style={{
              minHeight: "440px",
              marginTop: "1rem",
              whiteSpace: "pre-wrap",
            }}
            rows={10}
            cols={50}
            onKeyDown={(e) => {
              handleTabKeyUp(e, textAreaRef);
            }}
          />
          <Menu
            mode="inline"
            defaultSelectedKeys={["Test Cases"]}
            selectedKeys={
              testCaseRes?.length > 0
                ? ["Result", "Test Cases"]
                : ["Test Cases"]
            }
            openKeys={
              testCaseRes?.length > 0
                ? ["Result", "Test Cases"]
                : ["Test Cases"]
            }
            defaultOpenKeys={["Test Cases"]}
            style={{ height: "100%", borderRight: 0, flex: "0.4" }}
            items={testColumn(
              currentSelectedProblemInfo?.test_cases?.map((val, i) => ({
                ...val,
                key: i,
                label: (
                  <>
                    {" "}
                    Inp : <span style={{ color: "#1677FF" }}>{val.inp}</span>,
                    Out : <span style={{ color: "#1677FF" }}>{val.out}</span>
                  </>
                ),
              })),
              testCaseRes?.map((val, i) => ({
                ...val,
                key: i,
                label: (
                  <div style={{ maxWidth: "200px" }}>
                    <div style={{ width: "100%", overflowX: "scroll" }}>
                      Case {i + 1} :{" "}
                      <span style={{ color: "#1677FF" }}>
                        {val.status || val.attempted ? "Run, " : "Didn't Run"}
                        {val.status || val.passed ? "Passed ✅" : "Failed ❌"}
                      </span>
                      {val.inp && (
                        <>
                          <span style={{ color: "#1677FF" }}>{val.inp}</span>,
                          Out :{" "}
                          <span style={{ color: "#1677FF" }}>{val.output}</span>
                        </>
                      )}
                    </div>{" "}
                  </div>
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
