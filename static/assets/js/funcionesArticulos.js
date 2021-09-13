$(document).ready(function () { 
    
    $('table.display tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
        $("#sinfiltroVer").hide(); 
    });
       
    var tabla_art = $('table.display').DataTable({    
            
            "dom": 'Bfrtip', //'B<"float-left"i><"float-right"f>t<"float-left"l><"float-right"p><"clearfix">',
            "responsive": false,
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
            },
            "order": [[ 0, "desc" ]],
            "scrollX": false,
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
    
    $('select[name=selectVert]').change(function() { 
        if (tabla_art.column(2).search() !== this.value ) {
            tabla_art
                .column(2)
                .search( this.value )
                .draw();
        }
    });

    $("input[name=agregarVertModal]").click(function(){        
        var cn = $(this).parents("tr").attr('id');   
        var vert = $('select[name=selectVertArt]').val(); 
        
        if (vert==0) { 
            $("#mensajeVertical"+cn+"").modal("show");
        } else {       
            $.ajax({
                        type: "POST",
                        url: "/operaciones/mantenimientos/articulos-verticales/verificarCN",  
                        data: "cn="+cn,
                        success: function(resp) {  
                            if (resp == 'KO') { 
                                $("#agregarVertModal"+cn+"").val('ERROR');
                                $("#agregarVertModal"+cn+"").prop('disabled', true);
                                $("#mensaje"+cn+"").modal("show");
                                //$("mensajeCN"+cn+"").html(textoError);                               
                            } else {
                                $("#agregarArtVert"+cn).modal("show");                                                      
                            }
                        }
                });  
            }                             
    });
      
    $("input[name=agregarArtVert]").click(function(){
        var idElem =  $("input[name=agregarArtVert]").val();
        var vert = $('select[name=selectVert]').val(); 
        var cn    = $("#vademecum-cn"+ idElem +"").val();
        var ean   = $("#ean"+ idElem +"").val();
        var prod  = $("#prod"+ idElem +"").val();
        var min   = $("#min"+ idElem +"").val();
        var max   = $("#max"+ idElem +"").val();
        var mul   = $("#mult"+ idElem +"").val();
        var act   = $("#act"+ idElem +"").val();
        var ah    = $("#ah"+ idElem +"").val();      
        var fede  = $("#fede"+ idElem +"").val();  
        var iva   = $("#iva"+ idElem +"").val();
        var data  =  "cn="+cn+"&ean="+ean+"&prod="+prod+"&min="+min+"&max="+max+"&mul="+mul+"&act="+act+"&ah="+ah+"&fede="+fede+"&iva="+iva+"&vert="+vert;
      
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/articulos-verticales/agregarArtVertical",  
            data: data,
            success: function(resp) {  
               
                $("#agregarArtVert"+idElem+"").fadeOut();
                location.reload();
            }
        });
    });  
    
    $("input[name=editarArtVer]").click(function(){
    
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/articulos-verticales/editarArtVert",  
            data: data,
            success: function(resp) {  
                location.reload();
            }
        });
    });

    $("input[name=borrarArtVer]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/articulos-verticales/borrarArtVer",  
            data: data,
            success: function(resp) {  
                actual.remove();
                location.reload();
            }
        });     
    });
   
    $("#sinFiltroVert").hide(); 
    $("#sinFiltroVer").hide(); 

    $("input[name=cerrarModal1]").click(function(){ 
        var cn = $("input[name=hiddenClose]").val();
        $("#agregarArtVert"+cn).modal('toggle');        
    });

    $("input[name=cerrarModal2]").click(function(){ 
        var cn = $("input[name=hiddenClose]").val(); 
       // $('#mensajeVertical'+ cn +'').modal().hide();     
        $('#mensajeVertical'+ cn +'').modal("toggle");
    });
});    