import pandas as pd

def restaurant_score(rest_dict):
  df = pd.read_pickle('resources/score.pkl')
  for key in rest_dict.keys():
    food_score, service_score, hygiene_score, cp_score = 0, 0, 0, 0
    f_word, s_word, h_word, c_word =[], [], [], []
    # each restaurant
    for c in range(5):
      comment = rest_dict[key]['review'][c]['text'].lower()
      # each comment
      for i in range(1, df.shape[0]):
        if df['food'][i] != '' and comment.count(df['food'][i]) > 0:
          food_score += df['food_score'][i]
          f_word.append(df['food'][i])
          # print('food',df['food'][i])
        if df['service'][i] != '' and comment.count(df['service'][i]) > 0:
          service_score += df['service_score'][i]
          # print('service',df['service'][i])
          s_word.append(df['service'][i])
        if df['hygiene'][i] != '' and comment.count(df['hygiene'][i]) > 0:
          hygiene_score+= df['hygiene_score'][i]
          # print('hygiene',df['hygiene'][i])
          h_word.append(df['hygiene'][i])
        if df['c_p_chi'][i] != '' and comment.count(df['c_p_chi'][i]) > 0:
          cp_score += df['food_score'][i]
          # print('c_p_chi',df['c_p_chi'][i])
          c_word.append(df['c_p_chi'][i])
    # print('food', food_score, 'service', service_score, 'hygiene', hygiene_score, 'cp', cp_score)
    rest_dict[key]['food_score'] = food_score
    rest_dict[key]['service_score'] = service_score
    rest_dict[key]['hygiene_score'] = hygiene_score
    rest_dict[key]['cp_score'] = cp_score
    # print('====', key,'====')
    # print(rest_dict[key]['restaurant_aspect'])
    # print(food_score, service_score, cp_score, hygiene_score)
    # print(f_word, s_word, c_word, h_word)
  return rest_dict

