require_relative 'common'
require_relative 'twint_parser'

def main()
  users = User.all
  users.each do |user|
    username = user.username
    user_id = user.id
    parse(username, user_id, true)
  end
end


if __FILE__ == $0
  main()
end
