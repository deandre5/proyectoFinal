from app.model.dietasModel import Dietas

import io
import xlwt

dietas = Dietas()


class ReporteDietas():
    def generarReporte(self):

        consulta = dietas.reporte()
        print(consulta)
        output = io.BytesIO()

        workbook = xlwt.Workbook()
        sh = workbook.add_sheet("Reporte de dietas")

        sh.write(0, 0, "Nombre de dieta")
        sh.write(0, 1, "Cantidad de usuarios")

        idx = 0

        for item in consulta:

            sh.write(idx+1, 0, str(item.get("nombre")))
            sh.write(idx+1, 1, str(item.get("cantidad")))
            idx += 1

        workbook.save(output)
        output.seek(0)

        return output
