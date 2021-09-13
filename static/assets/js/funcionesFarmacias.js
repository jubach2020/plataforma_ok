$(document).ready(function () {  
    $('#listadoFarmacias tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );     
    });
  
    var table_farm = $('#listadoFarmacias').DataTable({    
            
            "dom": 'Bfrtip', //'B<"float-left"i><"float-right"f>t<"float-left"l><"float-right"p><"clearfix">',
            "responsive": false,
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
            },
            "order": [[ 0, "desc" ]],
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
        }
    });
    $("#sinFiltroFar").hide();

        
    
        $('select[name=selectVert]').change(function() { 
            var val = $('#selectVert').val();  
            if ( table_farm.column(3).search() !== this.value ) {
                table_farm
                    .column(3)
                    .search( this.value )
                    .draw();
            }
        });
        
           
  
        
            $("input[name=borrarFar]").click(function(){
                var actual = $(this).parents("tr");
                var idElem = parseInt(this.id);
                var data = "id="+idElem;
                $.ajax({
                    type: "POST",
                    url: "/operaciones/mantenimientos/farmacias-verticales/borrarFar",  
                    data: data,
                    success: function(resp) {  
                        actual.remove();
                        location.reload();
                    }
                });     
            });
        
           $("input[name=editarFar]").click(function(){
                
                var idElem = parseInt(this.id);
                var nif    = $("#nif"+ idElem +"").val();
                var desc   = $("#desc"+ idElem +"").val();
                var activo = $("#activo"+ idElem +"").val();
                var vert   = $("#vert"+ idElem +"").val();
                var prov   = $("#prov"+ idElem +"").val();
                var nom    = $("#nom"+ idElem +"").val();
                var may    = $("#may"+ idElem +"").val();        
                var data   =  "id="+idElem+"&nif="+nif+"&desc="+desc+"&activo="+activo+"&vert="+vert+"&prov="+prov+"&nom="+nom+"&may="+may;
                $.ajax({
                    type: "POST",
                    url: "/operaciones/mantenimientos/farmacias-verticales/editarFarmacia",  
                    data: data,
                    success: function(resp) {  
                        location.reload();
                    }
                });
            });

        /*$('input[name=nuevaFar]').click(function(){
            
            var nif    = $("#nif").val();
            var desc   = $("#desc").val();
            var activo = $("#activo").val();
            var vert   = $("#vert").val();
            var prov   = $("#prov").val();
            var nom    = $("#nom").val();
            var may    = $("#may").val();        
            var data   =  "nif="+nif+"&desc="+desc+"&activo="+activo+"&vert="+vert+"&prov="+prov+"&nom="+nom+"&may="+may;
            $.ajax({
                type: "POST",
                url: "/operaciones/mantenimientos/farmacias-verticales/agregarVertical",  
                data: data,
                success: function(resp) {  
                    location.reload();
                }
            });
        })*/

        $("#closeGral").click(function(){
            location.reload();        
        });

        $(".editar").click(function(){
            $("#editarFarModal").fadeOut();
            location.reload();
        })
        $("#nuevaFar").click(function(){
            $("#nuevaFarModal").fadeOut();
            location.reload();
        });
   
       $('#datosFarmacia').draggable(true);
                         


});

