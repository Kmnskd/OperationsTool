$(function() {
    $("#uploadForm").bind('click',function(){
      $.post('/upload/upload_package', {
        package_url: $('input[name="package_url"]').val(),
        username: $('input[name="username"]').val(),
        password: $('input[name="password"]').val(),
      }, function(res) {
         $('input[name="package_url"]').val('')
         $('input[name="username"]').val('')
         $('input[name="password"]').val('')
         $("#toast").addClass("show")
         $("#toast").removeClass("hide")
        setTimeout(function(){
            $("#toast").addClass("hide")
            $("#toast").removeClass("show")
        }, 5000)
      });
    })
});

function getVersionReq(){
        $("#cloud_version").empty()
        $("#frontend_version").empty()
        $("#cloud_version").append('<option value="0">不回滚</option>')
        $("#frontend_version").append('<option value="0">不回滚</option>')
       $.post('/rollout/image_version', {
            environment: $("#environment").val()
        }, function(res) {
            var version_info = res.version_info;
            console.log(version_info);
            cloud_tag = version_info.cloud_tag;
            frontend_tag = version_info.frontend_tag;
            console.log(cloud_tag);
            console.log(frontend_tag);
            cloud_tag.map(item=>{$("#cloud_version").append(`<option key='${item}'>${item}</option>`)});
            frontend_tag.map(item=>{$("#frontend_version").append(`<option key='${item}'>${item}</option>`)});
});}


$(function() {
    getVersionReq()
        $("#environment").bind('change',function(){
            getVersionReq();
    })
});


$(function() {
    $("#featureDeploy").bind('click',function(){
      $.post('/feature/feature_deploy', {
        commit: $('input[name="commit"]').val(),
        tag: $('input[name="tag"]').val(),
        environment: $('select[name="environment"]').val(),
      }, function(res) {
         $('input[name="commit"]').val('')
         $('input[name="tag"]').val('')
         $("#toast").addClass("show")
         $("#toast").removeClass("hide")
        setTimeout(function(){
            $("#toast").addClass("hide")
            $("#toast").removeClass("show")
        }, 5000)
      });
    })
});


$(function() {
  $("#updatePasswd").bind('click', function(){
    $('#errMsg').text("")
    $('#sucMsg').text("")
    var frm = $('#userForm');
    $.ajax({
       type: "post",
       url: "/ldap_manage/update_passwd",
       data: frm.serialize(),
       success: function(data){
            console.log('Submission was successful.');
            console.log(data);
            $('#sucMsg').text(data.message);
            alert(data.message);
       },
       error: function(data) {
            console.log('An error occurred.');
            console.log(data);
            $('#errMsgDiv').show();
            $('#errMsg').text(data.responseJSON.message)
	   },
	   complete: function(data) {
//			$("#updatePasswd").prop('disabled', false);
	   }
    })
  })
});


$(function() {
  $("#resetPasswd").bind('click', function(){
    $('#errMsg').text("")
    $('#sucMsg').text("")
    var frm = $('#nameForm');
    $.ajax({
       type: "post",
       url: "/ldap_manage/reset_passwd",
       data: frm.serialize(),
       success: function(data){
            console.log('Submission was successful.');
            console.log(data);
            $('#sucMsg').text(data.message)
            alert(data.message);
       },
       error: function(data) {
            console.log('An error occurred.');
            console.log(data);
            $('#errMsgDiv').show();
            $('#errMsg').text(data.responseJSON.message)
	   },
	   complete: function(data) {
//			$("#updatePasswd").prop('disabled', false);
			$('#myModal,.modal-backdrop').hide();
	   }
    })
  })
});
