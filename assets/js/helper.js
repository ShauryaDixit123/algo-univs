export const handleConvert = () => {
  const lines = inputText.split("\n");
  const indentedLines = lines.map((line) => "    " + line);
  const indentedString = indentedLines.join("\n");
  setIndentedText(indentedString);
};

export const handleTabKeyUp = (e, ref) => {
  if (e.key === "Tab" && !e.shiftKey) {
    e.preventDefault();
    const value = ref.current.value;
    const selectionStart = ref.current.selectionStart;
    const selectionEnd = ref.curren.selectionEnd;
    ref.current.value =
      value.substring(0, selectionStart) + "  " + value.substring(selectionEnd);
    ref.current.selectionStart =
      selectionEnd + 2 - (selectionEnd - selectionStart);
    ref.current.selectionEnd =
      selectionEnd + 2 - (selectionEnd - selectionStart);
  }
  if (e.key === "Tab" && e.shiftKey) {
    e.preventDefault();
    const value = ref.current.value;
    const selectionStart = ref.current.selectionStart;
    const selectionEnd = ref.current.selectionEnd;

    const beforeStart = value
      .substring(0, selectionStart)
      .split("")
      .reverse()
      .join("");
    const indexOfTab = beforeStart.indexOf("  ");
    const indexOfNewline = beforeStart.indexOf("\n");

    if (indexOfTab !== -1 && indexOfTab < indexOfNewline) {
      ref.current.value =
        beforeStart
          .substring(indexOfTab + 2)
          .split("")
          .reverse()
          .join("") +
        beforeStart.substring(0, indexOfTab).split("").reverse().join("") +
        value.substring(selectionEnd);

      ref.current.selectionStart = selectionStart - 2;
      ref.current.selectionEnd = selectionEnd - 2;
    }
  }
};
