package iit.qualitrack.frontend.data.api

import okhttp3.Interceptor
import okhttp3.Response

/**
 * Intercepts every HTTP request and, if TokenManager.token is set,
 * adds it as the Authorization header.
 */
class AuthInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        val builder = original.newBuilder()
        TokenManager.token?.let { bearer ->
            builder.header("Authorization", bearer)
        }
        return chain.proceed(builder.build())
    }
}
