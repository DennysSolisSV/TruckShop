$(document).ready(function(){
 	
	// get price and parts existence in part_task form

	$(document).on('change', '.part_task_select', function(event) {
      partTaskAjax();		
    });// end change event


  $(document).on('click', 'input:text[name=quantity]', function(event){
      partTaskAjax();
  });// end change event

  

  // cheking existence
  function partTaskAjax(){ 

    // getting data from the form
    var partForm = $(".parts_task");
    var actionEndPoint = partForm.attr("data-endpoint");
    var httpMethod = partForm.attr("method");
    // asigned the selected value.
    var formData = { id : $(".part_task_select option:selected").val() }
    var partSpan = partForm.find(".Part");
    var quantitySpan = partForm.find(".Quantity");
      // ajax request
    if (formData.id != ""){
      $.ajax({
          url: actionEndPoint,
          method: "GET",
          data: formData,
          success: function(data){
            partSpan.html("Price: " + data.price)
            quantitySpan.html("Existence: " + data.existence)
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
             console.log("bad")
          }
      }); // end ajax
  }
});
