const clases = JSON.parse('{{ clases_json|escapejs }}');
    const sesiones = JSON.parse('{{ sesiones_json|escapejs }}');

    window.onload = cargarTabla;

    function cargarTabla() {
        const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
        const horas = [
            '08:00 - 09:00', '09:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', 
            '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', 
            '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00'
        ]; // Horas fijas

        let tablaHTML = '<table>';
        tablaHTML += '<thead><tr><th class="hour-column">Hora</th>';
        dias.forEach(dia => {
            tablaHTML += `<th class="hour-column">${dia}</th>`;
        });
        tablaHTML += '</tr></thead><tbody>';

        horas.forEach((hora, index) => {
            tablaHTML += `<tr><td>${hora}</td>`;
            dias.forEach(dia => {
                tablaHTML += `<td data-hora="${hora}" data-dia="${dia}" class="hora-${index} dia-${dia}"></td>`;
            });
            tablaHTML += '</tr>';
        });

        tablaHTML += '</tbody></table>';
        document.getElementById('tabla-container').innerHTML = tablaHTML;

        // Pintar las celdas según las sesiones
        clases.forEach(clase => {
            const sesionesClase = sesiones.filter(sesion => sesion.fields.id_clase === clase.pk); // Filtrar sesiones por clase
            console.log(clase.pk)

            sesionesClase.forEach(sesion => {
                const dia = sesion.fields.dia;
                console.log(dia)
                const horaInicio = sesion.fields.hora_inicio;
                const horaFin = sesion.fields.hora_fin;
                console.log(horaInicio)
                console.log(horaFin)
                
                const [horaInicioHoras, minutoInicio] = horaInicio.split(':');
                const [horaFinHoras, minutoFin] = horaFin.split(':');
                
                const rangoInicio = `${horaInicioHoras}:${minutoInicio}`; // "10:00"
                const rangoFin = `${horaFinHoras}:${minutoFin}`;         // "11:00"
        
                console.log(rangoInicio);
                console.log(rangoFin);

                const filaInicio = horas.indexOf(`${rangoInicio} - ${parseInt(horaInicioHoras) + 1}:00`); 
                const filaFin = horas.indexOf(`${rangoFin} - ${parseInt(horaFinHoras) + 1}:00`);
                console.log(filaInicio)
                console.log(filaFin)

                const colorClase = obtenerColor(clase.pk);

                for (let i = filaInicio; i < filaFin; i++) {
                    const celda = document.querySelector(`.hora-${i}.dia-${dia}`);
                    console.log(celda)
                    if (celda) {
                        celda.classList.add(`clase-${clase.pk}`);  // Usar el PK de la clase para identificarla
                        celda.style.backgroundColor = colorClase;
                        celda.title = `Clase: ${clase.fields.nombre} - Profesor: ${sesion.fields.profesor}`;
                    }
                }
            });
        });

        // Agregar las referencias de las clases
        mostrarReferencias();
    }

    function mostrarReferencias() {
        let referenciasHTML = '<h3>Referencias de Clases:</h3><ul>';

        clases.forEach(clase => {
            referenciasHTML += `<li><strong>${clase.fields.nombre}</strong> <span style="display: inline-block; width: 20px; height: 20px; background-color: ${obtenerColor(clase.pk)};"></span><ul>`;
            sesiones.forEach(sesion => {
                if (sesion.fields.clase === clase.pk) {
                    referenciasHTML += `<li>Sesión: ${sesion.fields.dia}, ${sesion.fields.hora_inicio} - ${sesion.fields.hora_fin}</li>`;
                }
            });
            referenciasHTML += '</ul></li>';
        });

        referenciasHTML += '</ul>';
        document.getElementById('references-container').innerHTML = referenciasHTML;
    }

    function obtenerColor(id_clase) {
        switch (id_clase) {
            case 1:
                return '#FFDDC1';  // Rosa Claro
            case 2:
                return '#C1E1FF';  // Azul Claro
            case 3:
                return '#C1FFC1';  // Verde Claro
            case 4:
                return '#FFB6C1';  // Rosa Pastel
            case 5:
                return '#98FB98';  // Verde Menta
            case 6:
                return '#FFFACD';  // Amarillo Claro
            case 7:
                return '#ADD8E6';  // Azul Claro Pastel
            case 8:
                return '#F0E68C';  // Amarillo Mostaza
            case 9:
                return '#E6E6FA';  // Lavanda
            case 10:
                return '#FF6347';  // Tomate
            case 11:
                return '#8A2BE2';  // Azul Violeta
            case 12:
                return '#FFD700';  // Amarillo Dorado
            case 13:
                return '#D3D3D3';  // Gris Claro
            case 14:
                return '#FF1493';  // Rosa Profundo
            case 15:
                return '#32CD32';  // Verde Lima
            case 16:
                return '#FFD700';  // Amarillo
            case 17:
                return '#FF4500';  // Naranja Rojo
            case 18:
                return '#2E8B57';  // Verde Mar
            case 19:
                return '#20B2AA';  // Verde Oscuro Aguamarina
            case 20:
                return '#A52A2A';  // Marrón
            default:
                return '#FFFFFF';  // Blanco si no se encuentra
        }
    }