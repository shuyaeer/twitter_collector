require 'json'
require_relative 'common'

# twintでtweet一覧を取得し情報をdbに挿入
def fetch_tweet(username)
  `twint -u #{username} --json -o json/#{username}.json`
end

def main(username, user_id)
  fetch_tweet(username)
  res = File.foreach("json/#{username}.json") do |row|
    res = JSON.load(row)
    tweet_id = res['id']
    media_index = 1
    res['photos'].each do |photo|
      next  if Post.exists?(tweet_id: tweet_id, media_index: media_index)
      message = "#{username}に新規投稿がありました\n#{photo}"
      send_slack(message)
      Post.create(
        user_id: user_id,
        status: 1,
        username: username,
        tweet_id: tweet_id,
        media_index: media_index,
        image_url: photo + ':large'
      )
      media_index += 1
    end
  end
end

def send_slack(message)
  uri = URI.parse("https://hooks.slack.com/services/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")
  request = Net::HTTP::Post.new(uri)
  request.body = "payload={\"channel\": \"#twitter_collector\", \"username\": \"webhookbot\", \"text\": \"#{message}\", \"icon_emoji\": \":ghost:\"}"

  req_options = {
    use_ssl: uri.scheme == "https",
  }

  response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
    http.request(request)
  end

  # response.code
  response.body
end

if __FILE__ == $0
  username = ARGV[0]
  if username.nil?
    puts "引数を渡してくだい。"
  else
    record = User.find_by(username: username)
    user_id = record.id
    main(username, user_id)
  end
end
