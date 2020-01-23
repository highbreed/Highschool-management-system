$(function(){
    $('#action_view').click(function(){
        $.ajax({
            url: '{% url 'admissions:teacher_details' %}',
            dataType: 'json',
            success: function(data){

            }
        });
    });
});