Clases = true # vago

puts "!!!!!!!!!!!!!!!!!!  clases.rb RECARGADO"

# Somos parte del cliente.
# No importa si cada clase es completamente editable, dado que
# la vista no te deja cambiar lo que no se permite.
# (y en produccion, aunque pudieras, el servidor no lo aceptaria xd)

$session = nil # popular con algo despues jaja

ROLE_NADIE = 0
ROLE_PRESIDENTE = 1
ROLE_VOCAL = 2
ROLE_COORDINADOR = 3
ROLE_VOLUNTARIO = 4
ROLE_NADIE2 = 5

$rolelut = [
    "xxx",
    "Presidente",
    "Vocal",
    "Coordinador",
    "Voluntario",
]

class LocalSession
    
    @@role = ROLE_NADIE
    @@name = nil
    @@token = nil
    
    def log_in(name, pass)
        # send login request
        # receive success, name, role and token
        @@role = ROLE_PRESIDENTE
        @@name = "test"
        @@token = "tokentoken"
    end
    def log_out
        # if i have a token,
        # grpc log out
        # then toss token
        @@role = ROLE_NADIE
        @@name = nil
        @@token = nil
    end
    
    def ensure_consistency!
        if @@token == nil
            @@role = ROLE_NADIE
            @@name = nil
        else
            @@name ||= "BADTOKEN"
        end
    end
    
    def logged_in?
        return !!@@token
    end
    
    def can_mod_users?
        return @@role == ROLE_PRESIDENTE
    end
    def can_mod_inventory?
        return @@role <= ROLE_VOCAL
    end
    def can_mod_events?
        return @@role == ROLE_PRESIDENTE || @@role == ROLE_COORDINADOR
    end
    def can_join_events?
        return @@role <= ROLE_VOLUNTARIO
    end
end



class Usuario
    attr_accessor :idusuario, :nombre, :apellido, :nombreUsuario,
        :telefono, :clave, :email, :rol, :activo
    
    def initialize(gRPCobj = nil)
        # se espera que gRPCobj sea una respesta de gRPC
        
        @idusuario = gRPCobj&.idusuario
        @nombreUsuario = gRPCobj&.nombreUsuario
        @nombre = gRPCobj&.nombre
        @apellido = gRPCobj&.apellido
        @telefono = gRPCobj&.telefono
        @clave = gRPCobj&.clave # no tendriamos por que recibir esto
        @email = gRPCobj&.email
        @rol = gRPCobj&.rol #!!!
        @activo = gRPCobj&.activo
    end
    
    def scramble! # para probar
        instance_variables.each do |var|
            vname = var.to_s.delete("@") + rand(100000).to_s
            instance_variable_set(var, vname)
        end
        return self
    end
    
end

class Rol
    attr_accessor :id, :nombre
    
    def initialize(id, nom)
        @id = id
        @nombre = nom
    end
end

class Inventario
    
end

class Evento
    
end
