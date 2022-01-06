$( document ).ready(function() {
    $("#Search").click(function(){
            readURL($("#inputGroupFile04")[0])
    });

    function readURL(input) {
          if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
              
              var formData = new FormData();
              var fileName = $("#inputGroupFile04")[0].files[0].name;
              formData.append('img', e.target.result)
              formData.append('name', fileName)

              $('#original').attr('src', e.target.result);
              $('#original_name').html("Input - "+fileName);
              $('#fileLbl').html(fileName)

              $.ajax({
                type: "POST",
                url: 'http://127.0.0.1:5000/find',
                data: formData,
                async: false,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data){
                    response = data[0];

                    $('#first_name').html("First Match - "+data[0][0]);
                    $('#second_name').html("Second Match - "+data[1][0]);

                    document. getElementById('first').setAttribute( 'src', 'data:image/jpg;base64,'+data[0][2])
                    document. getElementById('second').setAttribute( 'src', 'data:image/jpg;base64,'+data[1][2])

                    $('#firScore').html(data[0][1]);
                    $('#secScore').html(data[1][1]);


                },
                error: function(xhr,status,error){
                    alert(error)
                },
                dataType: 'json'
              });

            }

            reader.readAsDataURL(input.files[0]); // convert to base64 string
          }
        }

    function upload(event){
        var result = event.target.result;
        var fileName = $("#inputGroupFile04")[0].files[0].name;

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:5000/find',
            data: {data: result, name:fileName},
            async: false,
            contentType: 'application/json',
            cache: false,
            processData: false,
            success: function(data){
                response = data[0];

                document. getElementById('first').setAttribute( 'src', 'data:image/jpg;base64,'+data[0][2])
                document. getElementById('second').setAttribute( 'src', 'data:image/jpg;base64,'+data[1][2])
            },
            error: function(xhr,status,error){
                alert(error)
            },
            dataType: 'json'
          });

    }
});