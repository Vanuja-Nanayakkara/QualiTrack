package iit.qualitrack.frontend.data.model

data class CreateFlagRequest(
    val operator_id: String,
    val machine_no: String,
    val defect: String,
    val inspected_by: String,
    val supervisor_in_charge: String,
    val date_of_inspection: String,
    val time_of_inspection: String,
    val flag_type: String,
    val issue_type: String?,
    val custom_reason: String?
)