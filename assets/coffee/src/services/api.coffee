angular.module('stxmuzyka').
    factory('api', (Restangular) ->
        Restangular.withConfig((RestangularConfigurer) ->
            RestangularConfigurer.setBaseUrl('/api/')

            # Makes DELETE requests body-less. Required by App Engine.
            RestangularConfigurer.setRequestInterceptor((elem, operation) ->
                if operation == 'remove'
                    return undefined
                elem
            )
        )
    )
