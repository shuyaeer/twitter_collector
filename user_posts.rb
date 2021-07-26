require_relative 'common'
# twitter の公式apiを仕様

class UserTimeline
  def initialize
    @username = ARGV[0]
  end

  def reqest_user_timeline(max_id=nil)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    uri = URI.parse(url)
    params = URI.decode_www_form(uri.query)
    params << ["screen_name", @username]
    params << ["count", 200]
    params << ["exclude_replies", true]
    params << ["include_rts", false]
    params << ["max_id", max_id] if max_id
    uri.query = URI.encode_www_form(params)
    request = Net::HTTP::Get.new(uri)
    bearer = ENV['BEARER']
    request["Authorization"] = "Bearer #{bearer}"

    req_options = {
      use_ssl: uri.scheme == "https",
    }

    response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
      http.request(request)
    end

    response.body
  end

  def save_image(media_url, i, tweet_id)
    image = URI.open(media_url).read
    File.write("#{@username}_#{tweet_id}_#{i}.jpg", image)
  end

  def insert_db(tweet_id, media_index, media_url)
    Post.create(
      status: 1,
      username: @username,
      tweet_id: tweet_id,
      media_index: media_index,
      image_url: media_url
    )
  end

  def extract_image(tweets)
    tweets.each do |tweet|
      media_index = 1
      tweet_id = tweet["id"]
      media_info = tweet["entities"]["media"]
      additional = tweet["extended_entities"]
      next if media_info.nil?
      media_info.each_with_index do |media|
        media_url = media["media_url"] + ':large'
        # return nil if Post.exists?(tweet_id: tweet_id, media_index: media_index)
        insert_db(tweet_id, media_index, media_url)
        # save_image(media_url, media_index, tweet_id)
        media_index += 1
      end
      next if additional.nil?
      additional_media = additional["media"][1..-1]
      additional_media.each do |media|
        media_url = media["media_url"] + ':large'
        # return nil if Post.exists?(tweet_id: tweet_id, media_index: media_index)
        insert_db(tweet_id, media_index, media_url)
        # save_image(media_url, media_index, tweet_id)
        media_index += 1
      end
    end
  end

  def sample()
    res_json = reqest_user_timeline()
    tweets = JSON.parse(res_json)
    tweets.each do |tweet|
      media_info = tweet["entities"]["media"]
      next if media_info.nil?
      media_info.each_with_index do |media|
        p media_url = media["media_url"]
      end
    end
  end

  def main()
    res_json = reqest_user_timeline()
    tweets = JSON.parse(res_json)
    return nil if tweets.empty?
    flg = extract_image(tweets)
    return nil unless flg
    max_id = tweets.last['id'].to_i - 1
    latest_id = max_id
    loop do
      res_json = reqest_user_timeline(max_id)
      tweets = JSON.parse(res_json)
      return nil if tweets.empty?
      flg = extract_image(tweets)
      return nil unless flg
      max_id = tweets.last['id'].to_i - 1
    end
  end

end

if __FILE__ == $0
  hoge = UserTimeline.new
  # hoge.main()
  hoge.sample()
end
