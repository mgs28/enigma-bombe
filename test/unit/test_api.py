import pytest

def test_index_of_coincidence(http_client):
    h = {"Matthew":0.04762, "Matthew Is Awesome":0.06667, "The secret of getting ahead is getting started.":0.09177, "Run your dbt Core projects as Apache Airflow DAGs and Task Groups with a few lines of code":0.05061}

    for s in h:
        #Given 
        # s
        
        #When
        response = http_client.get("/ioc?s={}".format(s))

        #Then
        assert response.status_code == 200
        assert round(float(response.text),5) == h[s], "{} != {}".format(s, h[s])
