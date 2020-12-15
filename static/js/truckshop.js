$(document).ready(function(){

  //setup before functions
  var typingTimer;                //timer identifier
  var doneTypingInterval = 1000;  //time in ms, 5 second for example


 	
	// get price and parts existence in part_task form

	$(document).on('change', '.part_task_select', function(event) {
      partTaskAjax();		
    });// end change event

  $(document).on('click', 'input:text[name=quantity]', function(event) {
    partTaskAjax();		
  });// end change event


  $(document).on('keyup', 'input:text[name=quantity]', function(){
    if (typingTimer) clearTimeout(typingTimer);                 // Clear if already set     
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
  });// end change event

  $(document).on('keydown', 'input:text[name=quantity]', function(){
    clearTimeout(typingTimer);
  });// end change event

  //user is "finished typing," do something
  function doneTyping () {
    partTaskAjax();
  }

  

  // cheking existence
  function partTaskAjax(){ 

    // getting data from the form
    var partForm = $(".parts_task");
    var actionEndPoint = partForm.attr("data-endpoint");
    var task = partForm.attr("data-task");
    var update = partForm.attr("data-update");
    var httpMethod = partForm.attr("method");
    // asigned the selected value.
    
    var partSpan = partForm.find(".Part");
    var quantitySpan = partForm.find(".Quantity");
    var buttonSubmit = partForm.find("#save");
    var errorLabel = partForm.find("#errors")
    var quantity = partForm.find("#id_quantity")

    


    var formData = { id : $(".part_task_select option:selected").val(), task : task, update: update}

    errorLabel.html("")
      // ajax request
    if (formData.id != ""){
      $.ajax({
          url: actionEndPoint,
          method: "GET",
          data: formData,
          success: function(data){
            // calc parts available
            if (update === "yes"){
              data.available = +data.available + +data.quantity;
            }

            partSpan.html("Price: " + data.price)
            quantitySpan.html("Available: " + data.available)
            
            if (data.part_exist_in_task === "yes" && update != "yes") {
              buttonSubmit.attr('disabled', true)
              errorLabel.html("Incident with this part already in this task.")
            }
            else {
              
              if(quantity.val() <= data.available){
                buttonSubmit.attr('disabled', false)
              }
              else {
                buttonSubmit.attr('disabled', true)
                errorLabel.html("Incident you do not have enough of this part in stock")
              }

              
            }
              
          },
          error: function(errorData){
             partSpan.html("")
             quantitySpan.html("")
          }
      }); // end ajax

    }
  }// end partTaskAjax

  // updating time labor in task
  var taskForm = $(".task-form");
  var timeLaborInput = taskForm.find("[name='time_labor']");
  var typingTimer;
  var typingInterval = 1000; // 0.5 second
  var taskBtn = taskForm.find("[type='submit']")
  var total_partSpan = taskForm.find("#id_total_parts");
  var total_laborSpan = taskForm.find("#id_total_labor");
  var total_taskSpan = taskForm.find("#id_total_task");

  timeLaborInput.keyup(function(event){
    // key released
    clearTimeout(typingTimer)

    if (timeLaborInput.val() != ""){
    typingTimer = setTimeout(performUpdate, typingInterval)
    }
  })

  timeLaborInput.keydown(function(event){
    // key pressed limpia una variable de tiempo
    clearTimeout(typingTimer)
  })

  function performUpdate(){ 
    
    // getting data from the form
    // var partForm = $(".parts_task");
    var actionEndPoint = taskForm.attr("data-endpoint");
    var httpMethod = taskForm.attr("method");
    var taskPk = taskForm.attr("task-pk");
    // asigned the selected value.
    var formData = { 
      time_labor : timeLaborInput.val(),
      task_pk: taskPk 
    }
    
      // ajax request
    
      $.ajax({
          url: actionEndPoint,
          method: httpMethod,
          data: formData,
          success: function(data){
            total_partSpan.val(data.total_parts)
            total_laborSpan.val(data.total_labor)
            total_taskSpan.val(data.total_task)
          },
          error: function(errorData){
             //alert("Should be number");
             alert(errorData);
          }
      }); // end ajax
  }
});




// el boton cancelar del detalle task