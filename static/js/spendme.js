// namespaces (to avoid errors on editing for example)
var mg = mg || {};
mg.sm = mg.sm || {};

mg.sm.editing = false;

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

mg.sm.attachEventHandlers = function() {
	$("#insert-expense-modal").on('shown.bs.modal', function() {
		$("input[name=expense]").focus();
	});	
};

mg.sm.enableButtons = function() {

	$('#when-input')
		.datepicker({
			format: 'yyyy-mm-dd',
			autoclose: true,
		})
    	.on('changeDate', function(ev) {
        	// var dateForBackend = new Date(ev.date);
        	// console.log(ev.date);
    	})
    ;

    $('#expense-input').on('change', function() {
  		$("#insert-expense-modal input[name=expense_number]").val($('#expense-input').autoNumeric('get'));
	});

	$('#expense-input').autoNumeric("init",{
        aSep: '',
        aDec: '.'//, 
        // aSign: '$ '
	});

	$("#toggle-edit").click(function() {
		if (mg.sm.editing) {
			mg.sm.editing = false;
			$(".edit-actions").toggleClass("hidden");
			$(this).html("Edit");
		} else {
			mg.sm.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
	});

	$("#add-expense").click(function() {
		$("#insert-expense-modal .modal-title").html("Agrega un gasto");
		$("#insert-expense-modal button[type=submit]").html("Agrega gasto");

		$("#insert-expense-modal input[name=expense]").val("");
		$("#insert-expense-modal input[name=when]").val(formatDate(new Date()));
		$("#insert-expense-modal select[name=category]").val();
		$("#insert-expense-modal textarea[name=comment]").val("");
		$("#insert-expense-modal input[name=expense_number]").val(0);
		$("#insert-expense-modal input[name=entity_key]").val("").prop("disabled", true);
	});

	$(".edit-expense").click(function() {
		$("#insert-expense-modal .modal-title").html("Edita este gasto");
		$("#insert-expense-modal button[type=submit]").html("Editar gasto");

		expense = $(this).find(".expense").html();
		when = $(this).find(".when").html();
		category = $(this).find(".category").html();
		comment = $(this).find(".comment").html();
		entityKey = $(this).find(".entity-key").html();

		$("#insert-expense-modal input[name=expense]").attr("placeholder", expense);
		$("#insert-expense-modal input[name=when]").val(when);
		$("#insert-expense-modal select[name=category]").val(category);
		$("#insert-expense-modal textarea[name=comment]").val(comment);
		$("#insert-expense-modal input[name=expense_number]").val(expense);
		$("#insert-expense-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});

	$(".delete-expense").click(function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-expense-modal input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function() {
	mg.sm.enableButtons();
	mg.sm.attachEventHandlers();
});



// fundamentals
// $("#toggle-edit").click(function() {
// 	$(".edit-actions").toggleClass("hidden");
// });