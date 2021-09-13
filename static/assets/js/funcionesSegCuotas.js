$(document).ready(function () {      

$('#listadoSegCuotas tfoot th').each( function () {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
});

    $('#listadoSegCuotas').DataTable({
    "destroy" : true,       
    "processing" : true,
    fixedHeader: true,
    "dom": 'B<"float-left"i><"float-right"f>t<"float-left"l><"float-right"p><"clearfix">',
    "responsive": true,
    "language": {
        "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
    },
    "order": [[ 0, "asc" ]],
    "initComplete": function () {
    this.api().columns().every( function () {
            var that = this;
            $( 'input', this.footer() ).on( 'keyup change', function () {
                if ( that.search() !== this.value ) {                        
                    that
                        .search( this.value )
                        .draw();
                    }
            });
        });
        $("#sinFiltroCuota1").hide();
    }    
});


$("input[name=calcularPorcen]").click(function(){
 
    var porcent    = $("input[name=porcentCuota]").val();
    var data      =  "porcentCuota="+porcent;
        $.ajax({
            type: "POST",
            url: "/operaciones/analisis/calculo-cuota",  
            data: data,
            success: function(resp) {  
               location.reload()
            }
        });
});

$('#pdfCuotas').click(function(){
    alert("bajar pdf");
});
  
});