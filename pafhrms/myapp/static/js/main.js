// (function($) {

// 	"use strict";

// 	var fullHeight = function() {

// 		$('.js-fullheight').css('height', $(window).height());
// 		$(window).resize(function(){
// 			$('.js-fullheight').css('height', $(window).height());
// 		});

// 	};
// 	fullHeight();

// 	$('#sidebarCollapse').on('click', function () {
//       $('#sidebar').toggleClass('active');
//   });

// })(jQuery);



// function validateNumberInput(input) {
// 	// Remove any non-digit characters
// 	input.value = input.value.replace(/\D/g, '');
   
// }



// $(document).ready(function() {
// $('.openModalButton').click(function() {
// var personnelId = $(this).data('afpsn'); // Assuming 'afpsn' is the unique identifier
// var address = $(this).data('address');
// var category = $(this).data('category');
// var rank = $(this).data('rank');

// var afsc = $(this).data('afsc');
// var unit = $(this).data('unit');
// var subunit = $(this).data('subunit');
// var contactnum = $(this).data('contactnum');
// var hpme = $(this).data('hpme');
// var promotion = $(this).data('promotion');

// $('#personnel_id').val(personnelId);
// // $('#firstnametxt').val(firstname);
// // $('#middlenametxt').val(middlename);
// // $('#lastnametxt').val(lastname);

// $('#addresstxt').val(address);
// $('#categorytxt').val(category);
// $('#ranktxt').val(rank);
// $('#afsctxt').val(afsc);
// $('#unitDP').val(unit);
// $('#contactnumtxt').val(contactnum);
// $('#hpmetxt').val(hpme);

// // Populate the subunit dropdown based on the selected unit
// populateSubunits(unit, subunit);

// $('#updateForm').submit(function(event) {
// event.preventDefault();

// var formData = $(this).serialize();
// var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

// $.ajax({
// url: '{% url "update_personnel" %}',
// method: 'POST',
// data: formData,
// headers: {
//   'X-CSRFToken': csrfToken
// },
// success: function(response) {
//   if (response.success) {
// 	console.log('Data updated successfully!');
// 	// location.reload(); // Reload page or update UI as needed
//   } else {
// 	console.error('Error updating data:', response.error);
//   }
// },
// error: function(xhr, status, error) {
//   console.error('Error updating data:', error);
// }
// });
// });
// });

// // Function to populate subunits based on the selected unit
// function populateSubunits(unit, selectedSubunit) {
// const unitSubunitMap = {
// 'HPAF': ['OCG', 'OVC', 'OCAS', 'OSAS', 'AFCC', 'OAFIG', 'OSS', 'AFSO', 'OESPA',
// 	   'AFSMO', 'AFPAO', 'OAFIA', 'OAFSM', 'OAFA', 'OAFPM', 'OAJA', 'OCAC',
// 	   'OCSAF', 'OCAFDS', 'OCNAF', 'OAFCE', 'OCHCA', 'AFREO', 'AFIMAO',
// 	   'AFCLOAC', 'OAFGAD', 'ACOFAS, A-1', 'ACOFAS, A-2', 'ACOFAS, A-3',
// 	   'ACOFAS, A-4', 'ACOFAS, A-5', 'ACOFAS, A-6', 'ACOFAS, A-7', 'ACOFAS, A-8',
// 	   'ACOFAS, A-9', 'ACOFAS, A-10'],
// 'AIBDC':  ['HAIBDC', '520th ABG', '530th ABG', '540th ABG', '550th ABG',
// 		 '560th ABG', '585th ABG', '590th ABG', '600ABG', '970th HECG',
// 		 'AFGH', '1301st DD'],
// 'ADC': ['HADC', '5FW', '580ACWW', '960AMDG', 'PADCC', 'ADAC'],
// 'AMC':['HAMC', '205THW', '220AW', '250PAW', '505SRG'],
// 'ACC': ['HACC', '15SW', '710SPOW'],
// 'AETDC': [ 'HAETDC', 'PAFOS', 'PAFOCS', 'PAFFS', 'PAFNCOS', 'PAFTSS',
// 		 'PAFBMS', 'PAFLTC', 'PAFALEN', '440AMG', 'TDC', 'AWC'],
// 'ARFC': ['HAFRC', '1st ARCEN', '2nd ARCEN', '3rd ARCEN', '4th ARCEN', '5th ARCEN', '6th ARCEN', '7th ARCEN', '8th ARCEN'],  
// 'PAFHRMC-A/U': [],
// 'GHQ': ['OJ1', 'OJ2', 'OJ3', 'OJ4', 'OJ5', 'OJ6', 'OJ7', 'OJ8', 'OJ9', 'OJ10', 'AFPCC','OTAG', 'OTPMG', 'OTCCHS', 'OTJAG', 'AFPPDO', 'OTQMG', 'OTSG', 'AFPSEO','AFPHRO', 'OTCN', 'OTCDS', 'OSPS', 'AFPIMAC', 'AFPREO', 'AFPEBSO', 'OTCE','AFP K9', 'AFPCOC', 'CEISO', 'CGEASH', 'OAFPSM', 'GHQTS', 'PMO', 'OSJA','ODCOP', 'ONAF', 'GHQPFO'],
// 'AFPWSSUS': ['PMA', 'AFPETDC', 'CEISSAFP', 'CRSAFP', 'ISAFP', 'AFPHSC', 'AFP SOCOM', 'AFPFC', 'AFPPS', 'AFPPKOC', 'AFPCES', 'AFPMCC', 'PSG', 'AFPPGMC', 'AFPCYBER', 'AFPRESCOM', 'DND'],
// };

// const subunitDP = document.getElementById('SubunitDP');
// subunitDP.innerHTML = '<option value="">--Select Subunit--</option>';

// if (unit) {
// const subunits = unitSubunitMap[unit];
// if (subunits) {
// subunits.forEach(function(subunit) {
//   const option = document.createElement('option');
//   option.value = subunit;
//   option.textContent = subunit;
//   subunitDP.appendChild(option);
// });
// }
// }

// if (selectedSubunit) {
// $('#SubunitDP').val(selectedSubunit);
// }
// }

// // Event listener for unit dropdown change
// $('#unitDP').change(function() {
// const selectedUnit = $(this).val();
// const selectedSubunit = $('#SubunitDP').val(); // Get the current value of subunit
// populateSubunits(selectedUnit, selectedSubunit); // Pass current subunit value to maintain selection
// });

// // Validate number input
// function validateNumberInput(input) {
// input.value = input.value.replace(/\D/g, '');
// }

// $('#contactnumtxt').on('input', function() {
// validateNumberInput(this);
// });
// });








