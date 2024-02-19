import React from "react";
import { Breadcrumb, Layout, Menu, theme, Tooltip } from "antd";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Space, Table, Tag, Flex, Input, Button, Select, Form } from "antd";

const CreateProblemForm = (props) => {
  const { TextArea } = Input;

  return (
    <div>
      <Flex vertical gap={10}>
        <h1>Create your own problem here too!</h1>
        <div>
          <Tooltip title={`Please saperate each values by "," Thanks!`}>
            <span>hover me!</span>
          </Tooltip>
        </div>
      </Flex>
      <Form
        name="form_problem"
        style={{
          maxWidth: 600,
          display: "flex",
          flexDirection: "column",
          gap: 20,
        }}
        onFinish={(values) => {
          console.log(values, "valueczxcxs");
          props.onSubmit(values);
        }}
        autoComplete="off"
      >
        <Form.Item name="name">
          <Input name="name" placeholder="title for problem" />
        </Form.Item>

        <Form.Item name="des">
          <TextArea name="des" placeholder="Write problem statement here" />
        </Form.Item>
        <Form.Item name="type">
          <Input name="type" placeholder="Tags for your problem" />
        </Form.Item>
        <Form.List name="test_cases">
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Space
                  key={key}
                  style={{ display: "flex", marginBottom: 8 }}
                  align="baseline"
                >
                  <Form.Item
                    {...restField}
                    name={[name, "inp"]}
                    rules={[
                      {
                        required: true,
                        message: "Missing input",
                      },
                    ]}
                  >
                    <Input placeholder="input" />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "out"]}
                    rules={[
                      {
                        required: true,
                        message: "Missing output",
                      },
                    ]}
                  >
                    <Input placeholder="Output" />
                  </Form.Item>
                  <MinusCircleOutlined onClick={() => remove(name)} />
                </Space>
              ))}
              <Form.Item>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  block
                  icon={<PlusOutlined />}
                >
                  Add Test Case
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Publish
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default CreateProblemForm;
