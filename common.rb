require 'net/http'
require 'uri'
require 'json'
require "active_record"
require 'logger'
require 'open-uri'

ActiveRecord::Base.establish_connection(
  adapter:  "mysql2",
  host:     "localhost",
  username: "root",
  password: "",
  database: "Twitter",
)

class Post < ActiveRecord::Base
end

class User < ActiveRecord::Base
end

ActiveRecord::Base.logger = Logger.new(STDERR)
