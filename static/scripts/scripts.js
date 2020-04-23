function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  if (evt == "firstOpen"){
  }
}

function unClick(Id, curId){
// Unclicks checkbox by Id given
  if (document.getElementById(curId).checked == false)
    document.getElementById(curId).checked = true;
  if (document.getElementById(curId).checked == true)
    document.getElementById(Id).checked = false;
}

function unclickAll(Id, curId){
  var content = document.getElementById(Id).childNodes[9];
  var input = content.getElementsByTagName('input');

  var i;
  for (i = 0; i < input.length; i ++){
    if (input[i].id == curId){
      input[i].checked = true;
    }
    else{
      input[i].checked = false;
    }
  }
}

function cb_uncheck_div(item){
  var content = item.parentElement.parentElement.childNodes;
  for (var i = 0; i < content.length; i++){
    if (content[i].attributes != undefined){
      content[i].childNodes[1].checked = false;
    }
  }
  item.checked = true;
}

function collapse(){
  var content = document.getElementById("GuideQuestions");

  var collapse = document.getElementsByClassName("collapsible")[0];
  console.log(collapse.style.marginBottom);
  if (collapse.style.marginBottom != "10px"){
      collapse.style.marginBottom = "10px";
  }
  if(collapse.style.marginBottom == "10px"){
      collapse.style.marginBottom = "0px";
  }

  if (content.style.display == ""){
    content.style.display = "block";
    return;
  }
  if (content.style.display == "none"){
    content.style.display = "block";
    return;
  }
  if (content.style.display == "block"){
    content.style.display = "none";
  }
}

function cbChange(obj) {
    var cbs = document.getElementsByClassName("checkbox");
    for (var i = 0; i < cbs.length; i++) {
        cbs[i].checked = false;
    }
    obj.checked = true;
}

function display_plasmid(){
  var options = document.getElementById('plasmid-present');
  if (options.checked == true){
    var plasmid = document.getElementsByClassName('optional-container')[0];
    plasmid.style.display = "block";
  }
  else{
    var plasmid = document.getElementsByClassName('optional-container')[0];
    plasmid.style.display = "none";
  }
}

function cb_uncheck(cur, other){
  if (cur.checked == false){
    cur.checked = true;
  }
  document.getElementById(other).checked = false;
  display_plasmid();
}

function set_height_euqal_to(other, cur){
  var main_h = document.getElementById(cur).style.height;
  var other_h = document.getElementById(other).style.height;
  if (main_h > other_h){
    document.getElementById(other).style.height = main_h
  }
  else{
    document.getElementById(main).style.height = other_h
  }
}

function display_input(item, other){
  console.log(item)
  console.log(other)
  var new_info = 's'
}
