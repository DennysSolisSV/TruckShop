$(document).ready(function(){
	
	// get price and parts existence in part_task form

	$(document).on('change', '.part_task_select', function(event) {

		// getting data from the form
		var partForm = $(".parts_task");
		var actionEndPoint = partForm.attr("data-endpoint");
        var httpMethod = partForm.attr("method");
        // asigned the selected value.
        var formData = { id : $(".part_task_select option:selected").val() }

     	// ajax request

     	$.ajax({
            url: actionEndPoint,
            method: "GET",
            data: formData,
            success: function(data){
              var partSpan = partForm.find(".Part");
              partSpan.html("Price: " + data.price)
              var quantitySpan = partForm.find(".Quantity");
              quantitySpan.html("Existence: " + data.existence)
            },
            error: function(errorData){
               console.log("error")
            }
      }); // end ajax
    });// end change event
});
