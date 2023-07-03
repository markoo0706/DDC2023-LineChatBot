# -*- coding: utf-8 -*-
"""Recommmendation_system_ver2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MQbI0Bgo1iN7sAX_oTnUh_2ghiXVU92R
"""

import copy
from scipy.spatial.distance import pdist, squareform
from math import cos, asin, sqrt, pi
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class Recommendation():
  def __init__(self, user, request, user_lat, user_lng, largest_similar_user_num = 11, flavor_list = ['義式料理', '日式料理', '中式料理', '西式料理'], rating_item = ['食物品質', '服務品質', '性價比', '環境氛圍', '衛生安全']):
    self.user = user # 使用者名稱
    self.request = str(request)
    self.user_lat = float(user_lat) # 使用者經度
    self.user_lng = float(user_lng) # 使用者緯度
    self.search_weekday = self.getWeekday() # 搜尋時間（週一-週日）
    self.search_time = datetime.datetime.now() # 搜尋時間（幾點幾分)
    self.largest_similar_user_num = largest_similar_user_num # 相似的多少位使用者
    self.flavor_list = flavor_list # 餐廳口味
    self.rating_item = rating_item # 餐廳評價項目

  def recommend(self, history_df, restaurant_df, penalty_df, recommended_df, num_restaurant_options_to_score = 10, distance_discount_500m = -0.2):
    # get restaurants
    restaurant_list = restaurant_df.index
    # normalize chatgpt score
    restaurant_df['chatgpt_score_noramlized'] = self.normalizeChatgptScore(restaurant_df, restaurant_list)

    # ===Calculate similarity between===
    similar_users = self.similarUsers(history_df)

    # ===Get potential similar restaurant based on user experience===
    potential_like_restaurant_dict = self.similarUsersExperiencedRestaurant(history_df, similar_users, restaurant_list)

    # ===Remove out of range===
    qualified_restaurant_dict = {} # 符合距離內的餐廳
    inrange_restaurant_dict = self.removeOutofRangeRestaurants(restaurant_df, qualified_restaurant_dict, restaurant_list)

    # ===Remove already recommended===
    qualified_restaurant_dict = self.removeAlreadyRecommended(recommended_df, inrange_restaurant_dict, restaurant_list)

    # =====Match search conidtion====
    # 符合距離、搜尋條件、沒有被推薦過
    matched_restaurant_dict = self.matchSearchCondition(restaurant_df, restaurant_list, qualified_restaurant_dict, self.request)
    # If less than num_restaurant_options_to_score options, search similar flavor
    similar_flavors = self.similarFlavor(restaurant_df) # 相似3 flavor
    if sum(value for value in matched_restaurant_dict.values()) < num_restaurant_options_to_score:
      waitlist_restaurant_dict = {}
      iswaitlist = True
      for asimilar_flavor in similar_flavors:
        # 根據qualified restaurant dict 給出候補名單
        tempt_waitlist_restaurant_dict = self.matchSearchCondition(restaurant_df, restaurant_list, qualified_restaurant_dict, asimilar_flavor)
        # Add tempt to waitlist if not in matched dict
        waitlist_restaurant_dict = self.addToWaitlist(waitlist_restaurant_dict, tempt_waitlist_restaurant_dict, restaurant_list, matched_restaurant_dict)
        # check if there are 5 restaurant
        if sum(waitlist_restaurant_dict.values()) + sum(matched_restaurant_dict.values()) >= num_restaurant_options_to_score:
          break

    # ===Give score for restaurant===
    # score matched restaurants
    score_matched_restaurant_dict = self.scoreCalculation(restaurant_list, restaurant_df, matched_restaurant_dict, distance_discount_500m)
    # score wiatlist restaurants
    if iswaitlist:
      score_waitlist_restaurant_dict = self.scoreCalculation(restaurant_list, restaurant_df, waitlist_restaurant_dict, distance_discount_500m)

    # ===Sort and give recommendation===
    recommend_list, message = self.sortAndRecommend(score_matched_restaurant_dict, score_waitlist_restaurant_dict, iswaitlist)

    return recommend_list, message

  def penalty(self, recommended_df, penalty_df, penalty_restaurant_dict):
    for rest in penalty_restaurant_dict.keys():
      recommended_df[rest][self.user] = 1
      penalty_restaurant_dict[rest][self.user] = penalty_restaurant_dict[rest]
    return 0

  def getWeekday(self):
    now = datetime.datetime.now()
    # 生成一個dict key為英文的星期 value為中文的星期
    week_dict = {"Monday":"星期一", "Tuesday":"星期二", "Wednesday":"星期三", "Thursday":"星期四", "Friday":"星期五", "Saturday":"星期六", "Sunday":"星期日"}
    return week_dict[now.strftime("%A")]
  def normalizeChatgptScore(self, restaurant_df, restaurant_list):
    ssr = StandardScaler()
    chatgpt_score_distribution = np.array([sum([restaurant_df[x][rest] - 3 for x in rating]) for rest in restaurant_list])
    chatgpt_score_noramlized = ssr.fit_transform(chatgpt_score_distribution.reshape(len(restaurant_list), 1))
    chatgpt_score_noramlized = chatgpt_score_noramlized.flatten()
    return chatgpt_score_noramlized

  def similarUsers(self, history_df):
    # 計算所有商品間的 jaccard distance
    jaccard_distances = pdist(history_df.values, metric='jaccard')
    # 原先距離最遠的會計算出 1，因此相似度就要以 1 - 原先值
    jaccard_similarity_array = 1 - squareform(jaccard_distances)
    # 將資料轉換成為 DataFrame 的格式
    jaccard_similarity_df = pd.DataFrame(jaccard_similarity_array, index=history_df.index, columns=history_df.index)
    # 找到想要檢視的使用者
    jaccard_similarity_series = jaccard_similarity_df.loc[self.user]
    # 排序從高到低
    ordered_similarities = jaccard_similarity_series.sort_values(ascending=False)
    # 相似度最高的10位使用者：扣除第一位是原使用者
    similar_users = ordered_similarities.index[1:self.largest_similar_user_num]
    return similar_users

  def similarUsersExperiencedRestaurant(self, history_df, similar_users, restaurant_list):
    waitlist = {}
    # 相似使用者的df
    similar_user_history_df = history_df.loc[similar_users]
    for rest in restaurant_list:
      waitlist[rest] = 0
      if history_df.loc[similar_users][rest].sum() > 0: # 有其中一人吃過
        waitlist[rest] = 1
      if history_df.loc[self.user][rest] == 1: # 排除使用者去過的
        waitlist[rest] = 0
    return waitlist

  def removeOutofRangeRestaurants(self, restaurant_df, inrange_restaurant_dict, restaurant_list):
    for rest in restaurant_list:
      inrange_restaurant_dict[rest] = 1
      if self.distance(self.user_lat, self.user_lng, restaurant_df['lat'][rest], restaurant_df['lng'][rest]) >= 1: # 距離超過1公里
        inrange_restaurant_dict[rest] = 0
    return inrange_restaurant_dict

  def distance(self, lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

  def removeAlreadyRecommended(self, recommended_df, qualified_restaurant_dict, restaurant_list):
    for rest in restaurant_list:
      if recommended_df[rest][self.user] >= 1:
        qualified_restaurant_dict[rest] = 0
        # print(rest, recommended_df[rest][user], qualified_restaurant_dict[rest])
    return qualified_restaurant_dict

  def matchSearchCondition(self, restaurant_df, restaurant_list, qualified_restaurant_dict, search_condition):
    matched_restaurant_dict = copy.deepcopy(qualified_restaurant_dict)
    if self.request != 'Random':
      for rest in restaurant_list:
        if restaurant_df[search_condition][rest] == 0:
          matched_restaurant_dict[rest] = 0
    return matched_restaurant_dict

  def similarFlavor(self, restaurant_df):
    flavor_df = restaurant_df[self.flavor_list].T
    # 計算所有商品間的 jaccard distance
    jaccard_distances = pdist(flavor_df.values, metric='jaccard')
    # 原先距離最遠的會計算出 1，因此相似度就要以 1 - 原先值
    jaccard_similarity_array = 1 - squareform(jaccard_distances)
    # 將資料轉換成為 DataFrame 的格式
    jaccard_similarity_df = pd.DataFrame(jaccard_similarity_array, index=flavor_df.index, columns=flavor_df.index)
    # 找到想要檢視的使用者
    jaccard_similarity_series = jaccard_similarity_df.loc[self.request]
    # 排序從高到低
    ordered_similarities = jaccard_similarity_series.sort_values(ascending=False)
    # 相似度最高的3個餐廳口味
    similar_flavor = ordered_similarities.index[1:4]
    return similar_flavor

  def addToWaitlist(self, waitlist_dict, bejoin_dict, restaurant_list, matched_dict):
    for rest in restaurant_list:
      # 如果已經在match dict 則waitlist不紀錄
      if matched_dict[rest] == 1:
        waitlist_dict[rest] = 0
        continue
      # # 如果沒記錄在waitlist:補上
      # if bejoin_dict[rest] == 1:
      #   waitlist_dict[rest] = 1
      try:
        if waitlist_dict[rest] == 0 and bejoin_dict[rest] == 1:
          waitlist_dict[rest] = 1
      except:
        waitlist_dict[rest] = 0
        if bejoin_dict[rest] == 1:
          waitlist_dict[rest] = 1
    return waitlist_dict

  def scoreCalculation(self, restaurant_list, restaurant_df, restaurant_dict, distance_discount_500m):
    score_restaurant_dict = {}
    for rest in restaurant_list:
      if restaurant_dict[rest] == 1:
        # chatgpt score
        score_restaurant_dict[rest] = restaurant_df['chatgpt_score_noramlized'][rest]
        # distance discount
        if self.distance(self.user_lat, self.user_lng, restaurant_df['lat'][rest], restaurant_df['lng'][rest]) > 0.5:
          score_restaurant_dict[rest] += distance_discount_500m
        # google rating
        score_restaurant_dict[rest] += restaurant_df['ratings'][rest]
      else:
        score_restaurant_dict[rest] = 0
    return score_restaurant_dict

  def sortAndRecommend(self, score_matched_restaurant_dict, score_waitlist_restaurant_dict, iswaitlist):
    sorted_score_matched_dict = dict(sorted(score_matched_restaurant_dict.items(), key=lambda item: item[1], reverse = True))
    # print(sorted_score_matched_dict.keys())
    if iswaitlist:
      sorted_score_waitlist_dict = dict(sorted(score_waitlist_restaurant_dict.items(), key=lambda item: item[1], reverse = True))
      # print(sorted_score_waitlist_dict)
    recommend_list = []
    # get top restaurants
    for key in sorted_score_matched_dict.keys():
      if sorted_score_matched_dict[key] > 0:
        recommend_list.append(key)
    if iswaitlist:
      for key in sorted_score_waitlist_dict.keys():
        if sorted_score_waitlist_dict[key] > 0:
          recommend_list.append(key)
    message = 'Fully recommended'
    if len(recommend_list) < 5:
      message ='Lack of recommend'
    return recommend_list, message