// this is for cortex

const checkForInputs = () => {
  const inputs = ["select", "radio", "text"];
  select_tags = document.getElementsByTagName("select");
  single_select = document.querySelectorAll("input.mrSingle"); // this is for web script question
  text_box = document.querySelectorAll("input.mrEdit"); //this for web script question
  cortex_radio = document.querySelectorAll(".radio");
  cortex_text = document.querySelectorAll("input[type='text']");

  if (select_tags.length > 0) {
    // do something for select tags
    alert("this is a select question");
    document.getElementsByTagName("select")[0].options[10].selected = true;
    document.getElementsByTagName("select")[1].options[25].selected = true;
  } else if (single_select.length > 0 || cortex_radio.length > 0) {
    alert(" this is a single select question");
  } else if (text_box.length == 1 || cortex_text.length > 0) {
    alert("this is a text box question");
  }
};

//  this is for main script

const checkForInputsInScript = () => {
  select_tags = document.querySelectorAll("select.mrDropdown");
  single_select = document.querySelectorAll("input.mrSingle"); // this is for web script question
  text_box = document.querySelectorAll("input.mrEdit"); //this for web script question
  next_button = document.querySelector("input[class='mrNext']");
  multi_select = document.querySelectorAll("input.mrMultiple");

  if (single_select.length > 0) {
    alert("this is a single select question");
  } else if (text_box.length > 0) {
    alert("this is a textbox question");
  } else if (select_tags.length > 0) {
    document.getElementsByTagName("select")[0].options[25].selected = true;
    document.getElementsByTagName("select")[1].options[10].selected = true;
    alert("this is a select question");
  } else {
    next_button.click();
  }
};
