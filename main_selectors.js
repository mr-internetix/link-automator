const checkForInputsInScript = () => {
  // check for visible and enabled function
  const visibleElements = (elements) => {
    return Array.from(elements).filter((element) => {
      const isVisible = element.checkVisibility();
      const isEnabled = !element.disabled;
      return isVisible && isEnabled;
    });
  };

  // selectors

  select_tags = visibleElements(document.querySelectorAll("select.mrDropdown"));
  single_select = visibleElements(document.getElementsByClassName("mrSingle"));
  text_box = visibleElements(document.getElementsByClassName("mrEdit"));
  next_button = visibleElements(document.getElementsByClassName("mrNext"));
  multi_select = visibleElements(document.querySelectorAll("mrMultiple"));
  all_labels = visibleElements(document.querySelectorAll("label"));
  grid_question = visibleElements(
    document.querySelectorAll(".mrGridCategoryText.mrGridQuestionText")
  );

  slider_question = visibleElements(document.getElementsByClassName("slider"));

  //   returning if available
  if (slider_question.length > 0) {
    slider_mover = document.querySelector(".slider-add-arrow");

    if (slider_mover.classList.contains("hidden-arrow")) {
      slider_mover.classList.remove("hidden-arrow");
    }

    return "slider";
  } else if (grid_question.length > 0) {
    return "grid_question";
  } else if (single_select.length > 0) {
    return "single_select";
  } else if (text_box.length > 0) {
    return "text_box";
  } else if (select_tags.length > 0) {
    return "select_tag";
  } else if (multi_select.length > 0) {
    return "multi_select";
  } else {
    return "null";
  }
};

checkForInputsInScript();
