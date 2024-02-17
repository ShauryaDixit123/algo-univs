import React from "react";
import ReactDOM from "react-dom";
import { App } from "./js/App";
import _ from "lodash";

function component() {
  const element = document.createElement("div");
  element.innerHTML = _.join([], " ");
  return element;
}
document.body.appendChild(component());

ReactDOM.render(<App />, document.getElementById("root"));
