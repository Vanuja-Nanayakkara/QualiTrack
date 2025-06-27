package iit.qualitrack.frontend.data.repository

import iit.qualitrack.frontend.data.api.ApiService
import iit.qualitrack.frontend.data.model.*
import okhttp3.MultipartBody
import retrofit2.Response

class GarmentRepository(private val api: ApiService) {
    // Auth
    suspend fun register(req: RegisterRequest) = api.register(req)
    suspend fun login(req: LoginRequest) = api.login(req)
    suspend fun getRole() = api.getUserRole()
    suspend fun assignRole(req: AssignRoleRequest) = api.assignRole(req)

    // Defects
    suspend fun listDefects(): Response<PaginatedResponse<Defect>> = api.listDefects()

    // alias so UI code compiles against getDefects()
    suspend fun getDefects(): Response<PaginatedResponse<Defect>> = api.listDefects()
    suspend fun createDefect(req: CreateDefectRequest) = api.createDefect(req)

    // Inspections
    suspend fun listInspections() = api.listInspections()
    suspend fun createInspection(req: CreateInspectionRequest) = api.createInspection(req)

    // Flags
    suspend fun listFlags() = api.listFlags()
    suspend fun createFlag(req: CreateFlagRequest) = api.createFlag(req)

    // Notifications
    suspend fun listNotifications(supId: Int) = api.listNotifications(supId)
    suspend fun readNotification(id: Int) = api.readNotification(id)
    suspend fun readAllNotifications(req: ReadAllRequest) = api.readAllNotifications(req)

    // Dashboards
    suspend fun inspectorDashboard(id: Int, date: String) = api.inspectorDashboard(id, date)
    suspend fun supervisorDashboard(id: Int, date: String) = api.supervisorDashboard(id, date)

    // Supervisors (paginated)
    suspend fun listSupervisors(): Response<PaginatedResponse<Supervisor>> = api.listSupervisors()

    // ML image analysis → FabricDefect
    suspend fun analyzeDefectImage(part: MultipartBody.Part): Response<Defect> =
        api.analyzeDefectImage(part)

    suspend fun getFromUrl(url: String): Response<PaginatedResponse<Inspection>> {
        return api.getPaginatedInspectionsByUrl(url)
    }

}