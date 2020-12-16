$(document).ready(function(){

  //setup before functions
  var typingTimer;                //timer identifier
  var doneTypingInterval = 700;  //time in ms, 5 second for example
 	
	// get price and parts existence in part_task form

	$(document).on('change', '.part_task_select', function(event) {
      partTaskAjax();		
  });// end change event

 
  $(document).on('click', 'input:text[name=quantity]', function(event) {
    partTaskAjax();		
  });// end change event


  $(document).on('keyup', 'input:text[name=quantity]', function(){
    if (typingTimer) clearTimeout(typingTimer);                 // Clear if already set     
    typingTimer = setTimeout(doneTypingPartTask, doneTypingInterval);
  });// end change event


  $(document).on('keydown', 'input:text[name=quantity]', function(){
    clearTimeout(typingTimer);
  });// end change event

  
  //user is "finished typing," do something
  function doneTypingPartTask () {
    partTaskAjax();
  }

  

  // cheking existence
  function partTaskAjax(){ 

    // getting data from the form
    var partForm = $(".parts_task");
    var actionEndPoint = partForm.attr("data-endpoint");
    var task = partForm.attr("data-task");
    var partbytask = partForm.attr("data-partbytask");
    var httpMethod = partForm.attr("method");
    // asigned the selected value.
    
    var partSpan = partForm.find(".Part");
    var quantitySpan = partForm.find(".Quantity");
    var buttonSubmit = partForm.find("#save");
    var errorLabel = partForm.find("#errors")
    var quantity = partForm.find("#id_quantity")

    


    var formData = { 
      id : $(".part_task_select option:selected").val(), 
      task : task, 
      partbytask: partbytask,

    }

    errorLabel.html("")
      // ajax request
    if (formData.id != ""){
      $.ajax({
          url: actionEndPoint,
          method: "GET",
          data: formData,
          success: function(data){

            // calc parts available that incluide the quantity save it before.
            //if (partbytask){
              data.available = +data.available + +data.quantity;
            //}

            partSpan.html("Price: " + data.price)
            quantitySpan.html("Available: " + data.available)
            
            if (data.part_exist_in_task === "yes") {
              buttonSubmit.attr('disabled', true)
              errorLabel.html("This part is already in this task.")
            }
            else {
              
              if(quantity.val() <= data.available){
                buttonSubmit.attr('disabled', false)
              }
              else {
                buttonSubmit.attr('disabled', true)
                errorLabel.html("Not enough parts in stock")
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
  var typingTimerL;
  var typingIntervalL = 700; 
  var taskBtn = taskForm.find("[type='submit']")
  var total_partSpan = taskForm.find("#id_total_parts");
  var total_laborSpan = taskForm.find("#id_total_labor");
  var total_taskSpan = taskForm.find("#id_total_task");

  $(document).on('keyup', 'input:text[name=time_labor]', function(){
    if (typingTimerL) clearTimeout(typingTimerL);                 // Clear if already set     
    typingTimerL = setTimeout(doneTypingLabor, doneTypingInterval);
  });// end change event

  $(document).on('keydown', 'input:text[name=time_labor]', function(){
    clearTimeout(typingTimerL);
  });// end change event

  //user is "finished typing," do something
  function doneTypingLabor () {
    performUpdate();
  }


  function performUpdate(){ 
    
    // getting data from the form
    var actionEndPoint = taskForm.attr("data-endpoint");
    var taskPk = taskForm.attr("task-pk");

    // check is input empty or add cero
    if (timeLaborInput.val()===""){
      time_labor = 0;
    } else {
      time_labor = timeLaborInput.val();
    }

    // asigned the selected value.
    var formData = { 
      time_labor : time_labor,
      task_pk: taskPk 
    }
    
      // ajax request
    
      $.ajax({
          url: actionEndPoint,
          method: "GET",
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
  // end updating time labor 
});




