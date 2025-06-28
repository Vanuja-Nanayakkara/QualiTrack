package iit.qualitrack.frontend.data.model

data class CreateInspectionRequest(
    val cli_inspector: Int, val supervisor: Int, val fabric_defect: Int, val status: String
)
