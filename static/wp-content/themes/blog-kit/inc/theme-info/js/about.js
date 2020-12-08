( function( $ ) {

	'use strict';

	$(document).ready(function () {

		$('.recommended-action-button').on('click',function() {
			var id = $(this).attr('id');
			var action = $(this).data('action');
			var nonce = $(this).data('nonce');

			$.ajax({
				type     : 'GET',
				dataType : 'html',
				url      : BlogKitAboutObject.ajaxurl,
				data     : {
					'action'   : 'wpcap_about_action_dismiss_recommended_action',
					'id'       : id,
					'_wpnonce' : nonce,
					'todo'     : action
				},
				success  : function () {
					location.reload();
				}
			});
		});
	});
} )( jQuery );
